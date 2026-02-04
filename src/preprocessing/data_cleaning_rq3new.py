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
from collections import Counter
from urllib.parse import urlparse

# --------------------------
# 第二步：配置全局参数
# --------------------------
class Config:
    # 1. 文件路径配置
    JSON_DIR = r""  # 分块JSON目录
    OUTPUT_DIR = r""  # 输出目录
    
    # 2. 分块文件前缀
    LIVEFEEDS_PREFIX = "livefeeds_"
    REPLY_PREFIX = "reply_"
    BOOSTERS_PREFIX = "boostersfavourites_"
    
    # 3. 活跃用户新规则（明确你的需求）
    ACTIVE_POST_REQUIRE = 1    # 至少发帖1次
    ACTIVE_INTERACTION_REQUIRE = 3  # 点赞+转发+回复总数≥3次

# --------------------------
# 第三步：工具函数（删除时间相关逻辑，新增行为类型统计）
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
    
    def extract_number(file_path):
        file_name = os.path.basename(file_path)
        return int(file_name.split('_')[-1].split('.')[0])
    
    sorted_chunk_files = sorted(chunk_files, key=extract_number)
    print(f"\nFound {len(sorted_chunk_files)} {file_prefix} chunk files:")
    for file in sorted_chunk_files:
        print(f"  - {os.path.basename(file)}")
    return sorted_chunk_files


def count_total_items(chunk_files):
    """预统计分块文件总数据条数（用于进度条）"""
    total = 0
    print("\nPre-counting total data items (for progress bar)...")
    for file in chunk_files:
        file_name = os.path.basename(file)
        with open(file, 'rb') as f:
            parser = ijson.items(f, 'item')
            chunk_count = sum(1 for _ in tqdm(parser, desc=f"Counting {file_name}"))
            total += chunk_count
    print(f"Pre-count completed: Total items = {total}")
    return total


def extract_instance_id(url_or_sid):
    """从URL或SID提取统一格式的实例ID（纯域名）"""
    url_or_sid_str = str(url_or_sid).strip()
    if '#' in url_or_sid_str:
        return url_or_sid_str.split('#')[0]
    else:
        parsed = urlparse(url_or_sid_str)
        return parsed.netloc if parsed.netloc else ""


def extract_user_instance(account):
    """从用户的account字典中提取所属实例（从url字段）"""
    user_url = account.get("url", "").strip()
    return extract_instance_id(user_url)  # 复用实例提取逻辑


def stream_chunk_data(chunk_files, total_items, desc):
    """流式读取分块数据（避免内存溢出）"""
    with tqdm(total=total_items, desc=desc) as pbar:
        for file in chunk_files:
            file_name = os.path.basename(file)
            print(f"\nReading chunk file: {file_name}")
            with open(file, 'rb') as f:
                parser = ijson.items(f, 'item')
                for item in parser:
                    yield item
                    pbar.update(1)


def update_user_behavior(user_behavior, user_id, behavior_type):
    """
    更新用户行为记录（拆分行为类型）
    behavior_type: "post"（发帖） / "interaction"（点赞/转发/回复）
    """
    # 初始化用户行为（默认发帖0次、互动0次）
    if user_id not in user_behavior:
        user_behavior[user_id] = {
            "post_count": 0,          # 发帖次数
            "interaction_count": 0    # 互动次数（点赞+转发+回复）
        }
    
    # 按行为类型累加计数
    if behavior_type == "post":
        user_behavior[user_id]["post_count"] += 1
    elif behavior_type == "interaction":
        user_behavior[user_id]["interaction_count"] += 1

# --------------------------
# 第四步：处理livefeeds数据（仅统计发帖行为）
# --------------------------
def process_livefeeds():
    """
    处理livefeeds：
    - 追踪用户发帖行为（更新post_count）
    - 记录用户-实例映射（从account.url提取）
    - 统计实例标签
    返回：user_behavior（用户行为）、user_to_instance（用户-实例映射）、instance_tags（实例标签）
    """
    livefeeds_chunks = get_chunk_files(Config.JSON_DIR, Config.LIVEFEEDS_PREFIX)
    if not livefeeds_chunks:
        raise FileNotFoundError("No livefeeds chunk files found! Check path and prefix.")
    
    livefeeds_total = count_total_items(livefeeds_chunks)
    
    # 初始化核心数据结构
    user_behavior = {}  # {user_id: {post_count, interaction_count}}
    user_to_instance = {}  # {user_id: instance_id}
    instance_tags = {}  # {instance_id: [tag1, tag2,...]}
    
    livefeeds_generator = stream_chunk_data(
        chunk_files=livefeeds_chunks,
        total_items=livefeeds_total,
        desc="Processing livefeeds (tracking posts & tags)"
    )
    
    for item in livefeeds_generator:
        # 1. 提取发布者信息（用户ID + 所属实例）
        account = item.get("account", {})
        user_id = account.get("id", "").strip()
        if not user_id:
            continue
        
        # 2. 提取用户所属实例并记录映射（避免重复）
        user_instance = extract_user_instance(account)
        if user_instance and user_id not in user_to_instance:
            user_to_instance[user_id] = user_instance
        
        # 3. 提取帖子所属实例（用于标签统计）
        post_instance = extract_instance_id(item.get("sid", ""))
        if not post_instance:
            continue
        
        # 4. 更新用户发帖行为（标记为"post"类型）
        update_user_behavior(user_behavior, user_id, behavior_type="post")
        
        # 5. 统计实例标签
        post_tags = [tag.get("name", "").strip() for tag in item.get("tags", [])]
        if post_instance not in instance_tags:
            instance_tags[post_instance] = []
        if post_tags:
            instance_tags[post_instance].extend([tag for tag in post_tags if tag])
    
    print(f"Livefeeds processed: Tracked {len(user_behavior)} users (with post records), {len(user_to_instance)} user-instance mappings")
    return user_behavior, user_to_instance, instance_tags

# --------------------------
# 第五步：处理互动数据（统计点赞/转发/回复，更新互动次数）
# --------------------------
def process_interactions(user_behavior, user_to_instance):
    """
    处理互动数据：
    - 追踪点赞/转发/回复（统一标记为"interaction"类型，更新interaction_count）
    - 补充互动用户的实例映射
    - 拆分3类互动计数器
    返回：3个互动计数器 + 更新后的user_behavior + 更新后的user_to_instance
    """
    # 初始化互动计数器（分类型）
    reply_counter = Counter()    # 回复：(from_inst, to_inst) → count
    boost_counter = Counter()    # 转发：(from_inst, to_inst) → count
    fav_counter = Counter()      # 点赞：(from_inst, to_inst) → count
    
    # 深拷贝避免修改原数据（保留livefeeds中的发帖记录）
    updated_user_behavior = {k: v.copy() for k, v in user_behavior.items()}
    updated_user_to_instance = user_to_instance.copy()
    
    # --------------------------
    # 子步骤1：处理回复互动（属于"interaction"类型）
    # --------------------------
    print("\n" + "="*50)
    print("Processing reply interactions (counted as 'interaction')...")
    reply_chunks = get_chunk_files(Config.JSON_DIR, Config.REPLY_PREFIX)
    if reply_chunks:
        reply_total = count_total_items(reply_chunks)
        reply_generator = stream_chunk_data(reply_chunks, reply_total, "Processing reply data")
        
        for item in reply_generator:
            # 发起回复方信息
            from_account = item.get("acct", {})
            from_user_id = from_account.get("id", "").strip()
            if not from_user_id:
                continue
            
            # 提取并补充发起方的实例映射
            from_instance = extract_user_instance(from_account)
            if from_instance and from_user_id not in updated_user_to_instance:
                updated_user_to_instance[from_user_id] = from_instance
            if not from_instance:
                continue  # 跳过无实例的回复
            
            # 被回复方实例（确定目标实例）
            to_account = item.get("reply_to_acct", {})
            to_instance = extract_user_instance(to_account)
            if not to_instance:
                continue  # 跳过无目标实例的回复
            
            # 更新用户互动行为（标记为"interaction"类型）
            update_user_behavior(updated_user_behavior, from_user_id, behavior_type="interaction")
            # 累加回复计数器
            reply_counter[(from_instance, to_instance)] += 1
    
    else:
        print("No reply chunk files found, skipping reply processing")
    
    # --------------------------
    # 子步骤2：处理转发+点赞互动（均属于"interaction"类型）
    # --------------------------
    print("\n" + "="*50)
    print("Processing boost & favourite interactions (counted as 'interaction')...")
    boosters_chunks = get_chunk_files(Config.JSON_DIR, Config.BOOSTERS_PREFIX)
    if boosters_chunks:
        boosters_total = count_total_items(boosters_chunks)
        boosters_generator = stream_chunk_data(boosters_chunks, boosters_total, "Processing boosters data")
        
        for item in boosters_generator:
            # 被互动帖子的目标实例（从sid提取）
            to_instance = extract_instance_id(item.get("sid", ""))
            if not to_instance:
                continue
            
            # 处理点赞互动
            favourites = item.get("favourites", [])
            for fav in favourites:
                try:
                    if not isinstance(fav, dict):
                        continue  # 只处理字典格式的用户数据
                    
                    fav_user_id = fav.get("id", "").strip()
                    if not fav_user_id:
                        continue
                    
                    # 补充点赞者的实例映射
                    fav_instance = extract_user_instance(fav)
                    if fav_instance and fav_user_id not in updated_user_to_instance:
                        updated_user_to_instance[fav_user_id] = fav_instance
                    if not fav_instance:
                        continue
                    
                    # 更新互动行为+累加计数
                    update_user_behavior(updated_user_behavior, fav_user_id, behavior_type="interaction")
                    fav_counter[(fav_instance, to_instance)] += 1
                except Exception as e:
                    print(f"\n?? Skip invalid favourite: {str(e)[:30]}, Data: {str(fav)[:50]}...")
                    continue
            
            # 处理转发互动
            reblogs = item.get("reblogs", [])
            for reblog in reblogs:
                try:
                    if not isinstance(reblog, dict):
                        continue  # 只处理字典格式的用户数据
                    
                    reblog_user_id = reblog.get("id", "").strip()
                    if not reblog_user_id:
                        continue
                    
                    # 补充转发者的实例映射
                    reblog_instance = extract_user_instance(reblog)
                    if reblog_instance and reblog_user_id not in updated_user_to_instance:
                        updated_user_to_instance[reblog_user_id] = reblog_instance
                    if not reblog_instance:
                        continue
                    
                    # 更新互动行为+累加计数
                    update_user_behavior(updated_user_behavior, reblog_user_id, behavior_type="interaction")
                    boost_counter[(reblog_instance, to_instance)] += 1
                except Exception as e:
                    print(f"\n?? Skip invalid boost: {str(e)[:30]}, Data: {str(reblog)[:50]}...")
                    continue
    
    else:
        print("No boostersfavourites chunk files found, skipping boost/fav processing")
    
    # 统计互动用户总数（含仅互动未发帖的用户）
    interaction_user_count = len([uid for uid, data in updated_user_behavior.items() if data["interaction_count"] > 0])
    print(f"\nInteraction processing completed: {interaction_user_count} users with interaction records, {len(updated_user_to_instance)} total user-instance mappings")
    return reply_counter, boost_counter, fav_counter, updated_user_behavior, updated_user_to_instance

# --------------------------
# 第六步：生成实例属性表（按新规则统计活跃用户）
# --------------------------
def generate_instance_attributes(user_behavior, user_to_instance, instance_tags):
    """
    生成实例属性表：
    - 用户总数：该实例下有行为（发帖/互动）的去重用户
    - 活跃用户数：满足“发帖≥1次 + 互动≥3次”的用户
    """
    print("\n" + "="*50)
    print("Generating instance_attributes.csv...")
    print(f"Active user rule: Post ≥{Config.ACTIVE_POST_REQUIRE} time + Interaction ≥{Config.ACTIVE_INTERACTION_REQUIRE} times")
    
    # 按实例分组统计用户
    instance_stats = {}
    for user_id, user_data in user_behavior.items():
        # 从映射中获取用户所属实例（跳过无实例的用户）
        instance_id = user_to_instance.get(user_id)
        if not instance_id:
            continue
        
        # 初始化实例统计（总用户+活跃用户均为去重集合）
        if instance_id not in instance_stats:
            instance_stats[instance_id] = {
                "total_users": set(),    # 总用户：有任何行为（发帖/互动）的用户
                "active_users": set()    # 活跃用户：满足新规则的用户
            }
        
        # 1. 加入总用户集合（只要有行为就统计）
        instance_stats[instance_id]["total_users"].add(user_id)
        
        # 2. 判断是否为活跃用户（严格按新规则）
        is_active = (
            user_data["post_count"] >= Config.ACTIVE_POST_REQUIRE
            and user_data["interaction_count"] >= Config.ACTIVE_INTERACTION_REQUIRE
        )
        if is_active:
            instance_stats[instance_id]["active_users"].add(user_id)
    
    # 组装属性数据
    attr_list = []
    for instance_id, stats in instance_stats.items():
        # 统计Top5主题标签（从livefeeds的标签数据提取）
        tag_list = instance_tags.get(instance_id, [])
        top5_tags = [tag for tag, _ in Counter(tag_list).most_common(5)]
        top5_tags_str = ",".join(top5_tags) if top5_tags else "无"
        
        attr_list.append({
            "实例ID": instance_id,
            "用户总数": len(stats["total_users"]),
            "活跃用户数": len(stats["active_users"]),
            "主题标签": top5_tags_str
        })
    
    # 数据清洗（去重+过滤无效数据）
    df = pd.DataFrame(attr_list)
    df = df.drop_duplicates(subset=["实例ID"])
    df = df.dropna(subset=["实例ID", "用户总数"])
    
    # 保存文件
    output_path = os.path.join(Config.OUTPUT_DIR, "instance_attributes.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Instance attributes saved: {output_path} (Total {len(df)} instances)")
    # 打印活跃用户统计概览
    total_active = sum([len(stats["active_users"]) for stats in instance_stats.values()])
    total_user = sum([len(stats["total_users"]) for stats in instance_stats.values()])
    print(f"Overall active user ratio: {total_active}/{total_user} ({total_active/total_user*100:.1f}%)")
    return output_path

# --------------------------
# 第七步：生成4个互动矩阵文件（逻辑不变，保持分类型输出）
# --------------------------
def generate_interaction_matrices(reply_counter, boost_counter, fav_counter):
    """生成回复/转发/点赞/总互动4个矩阵文件"""
    print("\n" + "="*50)
    print("Generating interaction matrix files...")
    
    # 定义矩阵配置：文件名、计数器、描述
    matrix_configs = [
        ("interaction_matrix_reply.csv", reply_counter, "Reply"),
        ("interaction_matrix_boost.csv", boost_counter, "Boost"),
        ("interaction_matrix_fav.csv", fav_counter, "Favourite"),
        ("interaction_matrix_total.csv", reply_counter + boost_counter + fav_counter, "Total")
    ]
    
    output_paths = {}
    for file_name, counter, desc in matrix_configs:
        # 组装矩阵数据
        matrix_data = []
        for (from_inst, to_inst), count in counter.items():
            matrix_data.append({
                "发起实例": from_inst,
                "目标实例": to_inst,
                "互动次数": count
            })
        
        # 数据清洗
        df = pd.DataFrame(matrix_data)
        df = df.drop_duplicates(subset=["发起实例", "目标实例"])
        df = df.dropna(subset=["发起实例", "目标实例", "互动次数"])
        df = df[(df["发起实例"] != "") & (df["目标实例"] != "")]
        
        # 保存文件
        output_path = os.path.join(Config.OUTPUT_DIR, file_name)
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        
        output_paths[desc] = output_path
        print(f"{desc} matrix saved: {output_path} (Total {len(df)} pairs)")
    
    return output_paths

# --------------------------
# 第八步：生成多维度实例互动统计表（逻辑不变，保持完整维度）
# --------------------------
def generate_instance_interaction_stats(reply_counter, boost_counter, fav_counter):
    """生成多维度互动统计表：内部/跨实例主动/被动各互动类型"""
    print("\n" + "="*50)
    print("Generating instance_interaction_stats.csv...")
    
    # 收集所有实例（发起+目标）
    all_instances = set()
    for counter in [reply_counter, boost_counter, fav_counter]:
        for (from_inst, to_inst) in counter.keys():
            all_instances.add(from_inst)
            all_instances.add(to_inst)
    all_instances = [inst for inst in all_instances if inst]  # 过滤空实例
    
    # 初始化统计字典
    stats_dict = {}
    for inst in all_instances:
        stats_dict[inst] = {
            # 内部互动（from=to）
            "内部回复数": 0,
            "内部转发数": 0,
            "内部点赞数": 0,
            "内部互动总数": 0,
            
            # 跨实例主动互动（from=当前实例，to≠当前实例）
            "跨实例主动回复数": 0,
            "跨实例主动转发数": 0,
            "跨实例主动点赞数": 0,
            "跨实例主动互动总数": 0,
            
            # 跨实例被动互动（to=当前实例，from≠当前实例）
            "跨实例被动回复数": 0,
            "跨实例被动转发数": 0,
            "跨实例被动点赞数": 0,
            "跨实例被动互动总数": 0,
            
            # 汇总
            "跨实例总互动数": 0
        }
    
    # 填充统计数据
    for inst in all_instances:
        # 1. 处理回复互动
        for (from_inst, to_inst), count in reply_counter.items():
            if from_inst == to_inst == inst:
                stats_dict[inst]["内部回复数"] += count
            elif from_inst == inst and to_inst != inst:
                stats_dict[inst]["跨实例主动回复数"] += count
            elif to_inst == inst and from_inst != inst:
                stats_dict[inst]["跨实例被动回复数"] += count
        
        # 2. 处理转发互动
        for (from_inst, to_inst), count in boost_counter.items():
            if from_inst == to_inst == inst:
                stats_dict[inst]["内部转发数"] += count
            elif from_inst == inst and to_inst != inst:
                stats_dict[inst]["跨实例主动转发数"] += count
            elif to_inst == inst and from_inst != inst:
                stats_dict[inst]["跨实例被动转发数"] += count
        
        # 3. 处理点赞互动
        for (from_inst, to_inst), count in fav_counter.items():
            if from_inst == to_inst == inst:
                stats_dict[inst]["内部点赞数"] += count
            elif from_inst == inst and to_inst != inst:
                stats_dict[inst]["跨实例主动点赞数"] += count
            elif to_inst == inst and from_inst != inst:
                stats_dict[inst]["跨实例被动点赞数"] += count
        
        # 4. 计算汇总字段
        stats_dict[inst]["内部互动总数"] = (
            stats_dict[inst]["内部回复数"] + stats_dict[inst]["内部转发数"] + stats_dict[inst]["内部点赞数"]
        )
        stats_dict[inst]["跨实例主动互动总数"] = (
            stats_dict[inst]["跨实例主动回复数"] + stats_dict[inst]["跨实例主动转发数"] + stats_dict[inst]["跨实例主动点赞数"]
        )
        stats_dict[inst]["跨实例被动互动总数"] = (
            stats_dict[inst]["跨实例被动回复数"] + stats_dict[inst]["跨实例被动转发数"] + stats_dict[inst]["跨实例被动点赞数"]
        )
        stats_dict[inst]["跨实例总互动数"] = (
            stats_dict[inst]["跨实例主动互动总数"] + stats_dict[inst]["跨实例被动互动总数"]
        )
    
    # 组装并清洗数据
    stats_list = []
    for inst, stats in stats_dict.items():
        stats["实例ID"] = inst
        stats_list.append(stats)
    
    df = pd.DataFrame(stats_list)
    # 调整列顺序（实例ID在前）
    col_order = ["实例ID"] + [col for col in df.columns if col != "实例ID"]
    df = df[col_order]
    # 数据清洗
    df = df.drop_duplicates(subset=["实例ID"])
    df = df.dropna(subset=["实例ID"])
    
    # 保存文件
    output_path = os.path.join(Config.OUTPUT_DIR, "instance_interaction_stats.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Interaction stats saved: {output_path} (Total {len(df)} instances)")
    
    # 打印示例数据（验证逻辑）
    if len(df) > 0:
        sample = df.iloc[0]
        print(f"\nSample (first instance):")
        print(f"  Instance ID: {sample['实例ID']}")
        print(f"  Internal Total: {sample['内部互动总数']}, Cross Total: {sample['跨实例总互动数']}")
    
    return output_path

# --------------------------
# 第九步：主函数（整合所有流程，删除时间相关打印）
# --------------------------
def main():
    print("="*60)
    print("        RQ3 Data Generation Script (Active User Rule Updated)")
    print("="*60)
    print(f"Active User Rule: Post ≥{Config.ACTIVE_POST_REQUIRE} time + Interaction (Like/Boost/Reply) ≥{Config.ACTIVE_INTERACTION_REQUIRE} times\n")
    
    try:
        # 1. 初始化输出目录
        create_dir(Config.OUTPUT_DIR)
        
        # 2. 处理livefeeds（发帖行为+用户-实例映射+标签）
        print("Step 1/5: Processing livefeeds data (track posts)")
        user_behavior, user_to_instance, instance_tags = process_livefeeds()
        
        # 3. 处理互动数据（互动行为+补充映射+拆分计数器）
        print("\nStep 2/5: Processing interaction data (track likes/boosts/replies)")
        reply_counter, boost_counter, fav_counter, updated_user_behavior, updated_user_to_instance = process_interactions(
            user_behavior=user_behavior,
            user_to_instance=user_to_instance
        )
        
        # 4. 生成实例属性表（按新规则统计活跃用户）
        print("\nStep 3/5: Generating instance attributes (active user rule applied)")
        attr_path = generate_instance_attributes(
            user_behavior=updated_user_behavior,
            user_to_instance=updated_user_to_instance,
            instance_tags=instance_tags
        )
        
        # 5. 生成4个互动矩阵文件
        print("\nStep 4/5: Generating interaction matrices (4 files)")
        matrix_paths = generate_interaction_matrices(reply_counter, boost_counter, fav_counter)
        
        # 6. 生成多维度互动统计表
        print("\nStep 5/5: Generating instance interaction stats")
        stats_path = generate_instance_interaction_stats(reply_counter, boost_counter, fav_counter)
        
        # 最终结果提示
        print("\n" + "="*60)
        print("        All RQ3 Files Generated Successfully!")
        print("="*60)
        print(f"1. Instance Attributes: {attr_path}")
        for desc, path in matrix_paths.items():
            print(f"2. {desc} Matrix: {path}")
        print(f"3. Interaction Stats: {stats_path}")
    
    except Exception as e:
        print(f"\n? Script Error: {str(e)}")
        print("Troubleshooting Tips:")
        print("1. Confirm JSON_DIR/OUTPUT_DIR in Config is correct")
        print("2. Ensure chunk file prefixes (e.g., 'livefeeds_') match your files")
        print("3. Check if user data in JSON is dict format (not string)")

# --------------------------
# 第十步：运行脚本
# --------------------------
if __name__ == "__main__":
    main()