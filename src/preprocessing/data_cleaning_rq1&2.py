# -*- coding: gbk -*-

# --------------------------
# 第一步：导入所有依赖库
# --------------------------
import os
import glob
import json
import ijson
import pandas as pd
from tqdm import tqdm
from urllib.parse import urlparse
import uuid  # 用于生成唯一event_id
from datetime import datetime  # 处理时间戳

# --------------------------
# 第二步：配置全局参数
# --------------------------
class Config:
    # 1. 文件路径配置（已填写用户实际路径）
    JSON_DIR = r"D:\shenty\fudan\DataNet-research\2025_autumn\241212livefeeds_splited"
    OUTPUT_DIR = r"D:\shenty\fudan\DataNet-research\2025_autumn\241212livefeeds_splited\RQ1"
    
    # 2. 分块文件前缀（与文件命名匹配）
    LIVEFEEDS_PREFIX = "livefeeds_"
    REPLY_PREFIX = "reply_"
    BOOSTERS_PREFIX = "boostersfavourites_"
    
    # 3. 异常值处理配置
    DEFAULT_TIMESTAMP = "2000-01-01T00:00:00Z"  # 无时间戳默认值（UTC格式）
    INTERACTION_TYPES = {"reply": "reply", "boost": "boost", "favourite": "favourite"}  # 修正拼写错误（favrourite→favourite）
    WEIGHT_DEFAULT = 1  # 互动强度默认值
    INSTANCE_VALID_LEN = 3  # 实例ID最小长度（避免无效值如"a.b"）
    INSTANCE_REQUIRE_DOT = True  # 实例ID必须包含"."（符合域名格式）

# --------------------------
# 第三步：工具函数（强化异常处理）
# --------------------------
def create_dir(path):
    """创建文件夹（若不存在）"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created output directory: {path}")
    else:
        print(f"Output directory already exists: {path}")


def get_chunk_files(json_dir, file_prefix):
    """获取分块文件并按数字排序"""
    file_pattern = os.path.join(json_dir, f"{file_prefix}*.json")
    chunk_files = glob.glob(file_pattern)
    if not chunk_files:
        print(f"Warning: No {file_prefix} files found in {json_dir}")
        return []
    
    def extract_number(file_path):
        """从文件名提取数字用于排序（适配“前缀_数字.json”格式）"""
        file_name = os.path.basename(file_path)
        try:
            return int(file_name.split('_')[-1].split('.')[0])
        except (IndexError, ValueError):
            return 0  # 非标准命名文件放最后
    
    sorted_chunk_files = sorted(chunk_files, key=extract_number)
    print(f"\nFound {len(sorted_chunk_files)} {file_prefix} chunk files:")
    for file in sorted_chunk_files[:3]:  # 只打印前3个避免输出过长
        print(f"  - {os.path.basename(file)}")
    if len(sorted_chunk_files) > 3:
        print(f"  - ... and {len(sorted_chunk_files)-3} more files")
    return sorted_chunk_files


def stream_chunk_data(chunk_files, desc):
    """流式读取分块数据（避免内存溢出，捕获文件读取异常）"""
    with tqdm(desc=desc, unit="item") as pbar:
        for file in chunk_files:
            file_name = os.path.basename(file)
            try:
                with open(file, 'rb') as f:
                    parser = ijson.items(f, 'item')
                    for item in parser:
                        yield item
                        pbar.update(1)
            except Exception as e:
                print(f"\nSkip corrupted file {file_name}: {str(e)[:50]}")
                continue


def is_valid_instance(instance_id):
    """判断实例ID是否有效（非空+长度达标+包含.）"""
    if not isinstance(instance_id, str):
        return False
    instance_clean = instance_id.strip()
    # 校验规则：非空 + 长度≥最小要求 + 包含"."（域名格式）
    return (
        len(instance_clean) >= Config.INSTANCE_VALID_LEN 
        and (not Config.INSTANCE_REQUIRE_DOT or "." in instance_clean)
        and instance_clean != "None"  # 排除由None转换的字符串
    )


def extract_instance_id(url_or_sid):
    """从URL或SID提取实例ID（强化异常处理，返回空字符串若无效）"""
    if not url_or_sid:
        return ""
    # 先转换为字符串，避免None或其他类型
    url_or_sid_str = str(url_or_sid).strip()
    # 处理SID格式（如“实例ID#帖子ID”）
    if '#' in url_or_sid_str:
        url_or_sid_str = url_or_sid_str.split('#')[0]
    # 解析URL获取域名
    try:
        parsed = urlparse(url_or_sid_str)
        # 若netloc为空（如纯域名字符串），直接用路径部分
        instance = parsed.netloc if parsed.netloc else parsed.path.strip()
        return instance if is_valid_instance(instance) else ""
    except Exception:
        # 解析失败时返回空字符串（视为无效实例）
        return ""


def extract_user_info(account):
    """从account字典提取用户ID、实例ID、时间戳（彻底避免None调用strip()）"""
    # 第一步：确保account是字典，否则直接返回无效值
    if not isinstance(account, dict):
        return "", "", Config.DEFAULT_TIMESTAMP
    
    # 第二步：提取用户ID（先转字符串再处理，避免None）
    user_id = str(account.get("id", "")).strip()  # 即使是None也转为"None"字符串
    if not user_id or user_id == "None":  # 过滤无效用户ID
        user_id = str(account.get("acct", "")).strip()
    # 再次过滤（确保用户ID非空且不是"None"）
    user_id = user_id if (user_id and user_id != "None") else ""
    
    # 第三步：提取实例ID（依赖extract_instance_id的有效性校验）
    user_url = str(account.get("url", "")).strip()
    user_instance = extract_instance_id(user_url)
    
    # 第四步：提取时间戳（先转字符串再处理，避免None）
    timestamp = str(account.get("last_status_at", "")).strip()
    if not timestamp or timestamp == "None":
        timestamp = str(account.get("created_at", "")).strip()
    # 统一时间格式或用默认值
    if not timestamp or timestamp == "None":
        timestamp = Config.DEFAULT_TIMESTAMP
    elif len(timestamp.split('T')) == 1:  # 补全UTC格式（如“2024-12-04”→“2024-12-04T00:00:00Z”）
        timestamp += "T00:00:00Z"
    
    return user_id, user_instance, timestamp


def generate_event_id(interaction_type, from_user_id, to_user_id, timestamp):
    """生成唯一event_id（避免特殊字符导致的格式问题）"""
    unique_suffix = str(uuid.uuid4())[:8]
    # 替换时间戳中的特殊字符（:→-，避免文件或数据库兼容问题）
    safe_timestamp = timestamp.replace(':', '-').replace('Z', '').replace('T', '-')
    # 生成基础ID（确保无空值占位）
    base_id = f"{interaction_type}_{from_user_id[:10]}_{to_user_id[:10]}_{safe_timestamp}"  # 截取用户ID前10位避免过长
    return f"{base_id}_{unique_suffix}"


# --------------------------
# 第四步：预处理Livefeeds（获取帖子→接收方映射，过滤无效接收方）
# --------------------------
def preprocess_livefeeds_for_interaction():
    """从livefeeds提取帖子SID与有效接收方的映射（to_instance无效则丢弃）"""
    livefeeds_chunks = get_chunk_files(Config.JSON_DIR, Config.LIVEFEEDS_PREFIX)
    if not livefeeds_chunks:
        return {}
    
    sid_to_recipient = {}
    data_generator = stream_chunk_data(livefeeds_chunks, "Preprocessing livefeeds (get valid post recipients)")
    
    for item in data_generator:
        # 1. 提取并校验帖子SID
        sid = str(item.get("sid", "")).strip()
        if not sid or sid in sid_to_recipient or sid == "None":
            continue
        
        # 2. 提取帖子作者（接收方）信息
        account = item.get("account", {})
        to_user_id, to_instance, to_timestamp = extract_user_info(account)
        
        # 3. 严格过滤无效接收方（用户ID非空 + 实例ID有效）
        if not (to_user_id and is_valid_instance(to_instance)):
            continue
        
        # 4. 加入映射（确保后续互动记录的to_instance有效）
        sid_to_recipient[sid] = (to_user_id, to_instance, to_timestamp)
    
    print(f"Preprocessed {len(sid_to_recipient)} valid post SID → recipient mappings (filtered invalid to_instance)")
    return sid_to_recipient


# --------------------------
# 第五步：提取各类互动记录（严格过滤无效实例）
# --------------------------
def extract_reply_records():
    """提取回复互动记录（to_instance无效则丢弃）"""
    reply_chunks = get_chunk_files(Config.JSON_DIR, Config.REPLY_PREFIX)
    if not reply_chunks:
        return []
    
    reply_records = []
    data_generator = stream_chunk_data(reply_chunks, "Extracting reply interactions (filter invalid to_instance)")
    
    for item in data_generator:
        # 1. 提取发起方信息（确保from_instance有效）
        from_account = item.get("acct", {})
        from_user_id, from_instance, from_timestamp = extract_user_info(from_account)
        if not (from_user_id and is_valid_instance(from_instance)):
            continue
        
        # 2. 提取接收方信息（严格校验to_instance）
        to_account = item.get("reply_to_acct", {})
        to_user_id, to_instance, to_timestamp = extract_user_info(to_account)
        # 关键：to_instance无效则直接丢弃该记录
        if not (to_user_id and is_valid_instance(to_instance)):
            continue
        
        # 3. 生成唯一event_id
        event_id = generate_event_id("reply", from_user_id, to_user_id, from_timestamp)
        
        # 4. 组装回复记录
        reply_records.append({
            "event_id": event_id,
            "timestamp": from_timestamp,
            "from_user_id": from_user_id,
            "from_instance": from_instance,
            "to_user_id": to_user_id,
            "to_instance": to_instance,
            "interaction_type": Config.INTERACTION_TYPES["reply"],
            "is_cross": from_instance != to_instance,
            "weight": Config.WEIGHT_DEFAULT
        })
    
    print(f"Extracted {len(reply_records)} valid reply interaction records (discarded invalid to_instance)")
    return reply_records


def extract_boost_fav_records(sid_to_recipient):
    """提取转发/点赞记录（to_instance无效则丢弃，依赖预处理的有效映射）"""
    boosters_chunks = get_chunk_files(Config.JSON_DIR, Config.BOOSTERS_PREFIX)
    if not boosters_chunks:
        return []
    
    bf_records = []
    data_generator = stream_chunk_data(boosters_chunks, "Extracting boost/favourite interactions (filter invalid to_instance)")
    
    for item in data_generator:
        # 1. 提取并校验帖子SID（仅用预处理过的有效映射）
        sid = str(item.get("sid", "")).strip()
        if not sid or sid not in sid_to_recipient or sid == "None":
            continue
        # 从映射获取接收方信息（已确保to_instance有效）
        to_user_id, to_instance, to_timestamp = sid_to_recipient[sid]
        # 二次校验to_instance（双重保险）
        if not (to_user_id and is_valid_instance(to_instance)):
            continue
        
        # 2. 提取点赞记录（过滤无效发起方和接收方）
        favourites = item.get("favourites", [])
        for fav in favourites:
            from_user_id, from_instance, from_timestamp = extract_user_info(fav)
            # 发起方无效或接收方无效则跳过
            if not (from_user_id and is_valid_instance(from_instance)):
                continue
            # 生成event_id
            event_id = generate_event_id("favourite", from_user_id, to_user_id, from_timestamp)
            bf_records.append({
                "event_id": event_id,
                "timestamp": from_timestamp,
                "from_user_id": from_user_id,
                "from_instance": from_instance,
                "to_user_id": to_user_id,
                "to_instance": to_instance,
                "interaction_type": Config.INTERACTION_TYPES["favourite"],
                "is_cross": from_instance != to_instance,
                "weight": Config.WEIGHT_DEFAULT
            })
        
        # 3. 提取转发记录（同上，过滤无效方）
        reblogs = item.get("reblogs", [])
        for reblog in reblogs:
            from_user_id, from_instance, from_timestamp = extract_user_info(reblog)
            if not (from_user_id and is_valid_instance(from_instance)):
                continue
            event_id = generate_event_id("boost", from_user_id, to_user_id, from_timestamp)
            bf_records.append({
                "event_id": event_id,
                "timestamp": from_timestamp,
                "from_user_id": from_user_id,
                "from_instance": from_instance,
                "to_user_id": to_user_id,
                "to_instance": to_instance,
                "interaction_type": Config.INTERACTION_TYPES["boost"],
                "is_cross": from_instance != to_instance,
                "weight": Config.WEIGHT_DEFAULT
            })
    
    print(f"Extracted {len(bf_records)} valid boost/favourite interaction records (discarded invalid to_instance)")
    return bf_records


# --------------------------
# 第六步：合并并清洗互动记录（最终过滤）
# --------------------------
def generate_interaction_table():
    """生成最终互动记录表（多重过滤确保数据质量）"""
    print("\n" + "="*60)
    print("Starting to generate interaction table (final data cleaning)")
    print("="*60)
    
    # 1. 预处理livefeeds（获取有效帖子→接收方映射）
    sid_to_recipient = preprocess_livefeeds_for_interaction()
    
    # 2. 提取各类互动记录（已过滤无效to_instance）
    reply_records = extract_reply_records()
    bf_records = extract_boost_fav_records(sid_to_recipient)
    all_records = reply_records + bf_records
    
    if not all_records:
        raise ValueError("No valid interaction records found! All records were discarded due to invalid data.")
    
    # 3. 转换为DataFrame进行最终清洗
    df = pd.DataFrame(all_records)
    initial_count = len(df)
    print(f"\nInitial total valid records before final cleaning: {initial_count}")
    
    # 4. 最终过滤（双重保险，排除漏网的无效数据）
    # 过滤实例ID无效的记录
    df = df[
        df["from_instance"].apply(is_valid_instance) & 
        df["to_instance"].apply(is_valid_instance)
    ]
    # 过滤用户ID为空或"None"的记录
    df = df[
        (df["from_user_id"] != "") & (df["from_user_id"] != "None") & 
        (df["to_user_id"] != "") & (df["to_user_id"] != "None")
    ]
    # 去重（基于event_id唯一标识）
    df = df.drop_duplicates(subset=["event_id"], keep="first")
    
    # 5. 检查清洗后的数据量
    final_count = len(df)
    print(f"Final valid records after cleaning: {final_count} (discarded {initial_count - final_count} invalid records)")
    if final_count == 0:
        raise ValueError("All records were discarded during final cleaning. Check your JSON data format.")
    
    # 6. 调整字段顺序（按分析优先级排序）
    field_order = [
        "event_id", "timestamp", "from_user_id", "from_instance",
        "to_user_id", "to_instance", "interaction_type", "is_cross", "weight"
    ]
    df = df[field_order]
    
    # 7. 保存为CSV（utf-8-sig避免中文乱码，兼容Excel）
    output_path = os.path.join(Config.OUTPUT_DIR, "interaction_table.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\nInteraction table saved to: {output_path}")
    
    # 8. 输出数据摘要（便于快速验证数据质量）
    print("\n" + "-"*40)
    print("Interaction Table Quality Summary:")
    print(f"Total valid records: {final_count}")
    print(f"Interaction type distribution:\n{df['interaction_type'].value_counts().to_string()}")
    print(f"Cross-instance interaction ratio: {df['is_cross'].sum()}/{final_count} ({df['is_cross'].mean()*100:.1f}%)")
    print(f"Unique from_instances: {df['from_instance'].nunique()}")
    print(f"Unique to_instances: {df['to_instance'].nunique()}")
    print("-"*40)
    
    return output_path


# --------------------------
# 第七步：主函数（整合流程，友好报错）
# --------------------------
def main():
    print("="*60)
    print("        Mastodon Interaction Table Generator (v2.0)")
    print("="*60)
    
    try:
        # 1. 初始化输出目录
        create_dir(Config.OUTPUT_DIR)
        
        # 2. 生成互动记录表（核心步骤）
        generate_interaction_table()
        
        print("\n" + "="*60)
        print("        Interaction Table Generated Successfully!")
        print("="*60)
    
    except ValueError as ve:
        # 捕获数据量不足的错误（友好提示）
        print(f"\nData Error: {str(ve)}")
        print("Suggestion: Check if your JSON files have valid 'account' and 'sid' fields.")
    except Exception as e:
        # 捕获其他未知错误
        print(f"\nUnexpected Error: {str(e)}")
        print("\nTroubleshooting Tips:")
        print("1. Confirm Config.JSON_DIR has your JSON chunks (livefeeds_, reply_, boostersfavourites_)")
        print("2. Check if JSON files are not corrupted (try opening with a text editor)")
        print("3. Ensure Python has read permissions for the JSON directory")


# --------------------------
# 第八步：运行脚本
# --------------------------
if __name__ == "__main__":
    main()