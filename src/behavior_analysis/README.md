# xhb 工作日志

10.24

1、制定规划

1）根据现有数据（暂时是boostersfavourites)，分析整理出一份有互动记录的实例列表，交由沈同学爬取对应实例信息。

2）根据现有数据，分析整理出，实例中用户互动情况，并进一步分析用户跨实例互动和在实例内互动的情况，构建实例互动网络。

3）根据爬取到的实例信息，分析实例用户互动比例与跨实例互动比例，结合实例大小、规则等因素，分析原因。

4）根据分析结果，勾勒不同跨实例互动程度实例的不同特征。

5）可视化

2、整理数据集

基于数据集boostersfavourites,分析其中sid（发起互动者）与id（被动参与互动者）所属实例，得到以下两个实例列表。

1）sum_based_stats：统计被动参与互动者。

例：

假设用户A收藏了来自实例X、Y、Z的3个用户，用户B收藏了实例Y、Z的2个用户：

`sum_based_stats` 会统计：X(1)、Y(2)、Z(2) → 3个唯一实例

[sum_based_stats.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/aacaff9f-b8d2-4bd5-9abf-f8ee71aed175)

2）sum_based_user:统计发起互动者

例：

`sum_based_user` 会统计：用户A归为X，用户B归为Y → 2个唯一实例

[sum_based_user.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/ffe5a307-a02e-4472-ae00-87d595753f4e)

[abstruct.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/055b5df7-2f9b-4e31-b0ac-614ba14b56b2)

[sum.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/209554a5-66d6-40c4-9391-155b9b93a790)

这是这一阶段用于数据分析的python代码。

abstruct文件可分析提取指定json文件，形成：实例名 + 计数  的格式。

sum文件可合并相同的实例，并叠加计数。

10.25

1、根据原始数据集，分析得到每个实例用户在本实例内的互动与跨实例互动数据。

得到数据集：

[sum_interaction.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/7ece3c9b-d6c4-4b55-be59-eb589aa6855d)

该数据集包含所有实例，实例互动总数，实例内互动数，跨实例互动数，跨实例互动比例。

2、对上述数据进行可视化处理，得到下图

![final_interaction_analysis_comprehensive.png](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/d73bce70-c35c-4a05-acda-23b2391980ac)

左上图为总互动中跨实例互动数（蓝色）与实例内互动数（橙色）的比例。

右上图为前20大实例中，跨实例互动数占总互动数的比例。

左下图为前30大实例中，用户间互动（包括实例内互动和跨实例互动）总数。

右下图为前15大实例中，跨实例互动（粉色）与实例内互动（蓝色）数量。

综上，我们得到用户互动的基本数据概况。

[sum_interaction.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/d980ae79-e8cc-4983-b775-1337503c9373)

这是完成本次分析的Python代码。

10.29

对来自天裕同学的数据集进行处理：

1、分别以活跃用户数和用户总数对实例从小到大进行排序，并对实例规模划分等级。

得到两个文件：

1）

[实例_按用户总数排序.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/f8c75d9e-6dc7-437b-a2ef-c1fbead221bf)

2）

[实例_按活跃用户数排序.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/cda220a9-e5e3-4876-90c3-4aa44131af68)

把两个文件合并分析，并得到实例用户活跃度比例：

[实例用户规模综合报告.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/ab52b49d-bd37-4d39-83af-aa20fc24eb6d)

以下是实现分析的python代码

[deal_instances.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/abeb5bdd-3853-4cb3-845d-af54206561d8)

2、从跨实例互动程度、实例内互动程度、跨实例互动占互动总数比例对实例从大到小进行排序，得到以下三个文件：

1）

[跨实例互动总数排序结果.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/7dd72df6-5a8a-4f7a-952c-3fc5b5a9f060)

2）

[内部互动总数排序结果.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/4b7322c6-0555-48d8-8d16-fb32f3b983cd)

3）

[实例_跨实例互动比例完整分析.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/17ff609e-80c6-4056-9a0d-2f711dd3816a)

以下是实现该分析的python代码

[deal_Interactions.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/1977cd06-fd56-43be-816c-cff51e331d6c)

[deal_interaction_acrossinstances_rate.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/f19562b5-cbd2-4464-b0e3-cab2214ca051)

3、对实例互动情况进一步分析，找出源节点、汇节点、孤立节点、双向节点。得到以下数据：

1）源节点

[源节点_按主动互动排序.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/89167527-b1c5-4686-b5ac-6f0cdf7ee54a)

[TOP20_源节点排行榜.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/d813e0bd-434c-4256-bb65-38833612193a)

2）汇节点

[汇节点_按被动互动排序.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/ff2bef24-c2af-4638-8428-a44ec1228239)

[TOP20_汇节点排行榜.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/73c4d1f0-faa6-4f17-a6a1-eed2944842b1)

3）孤立节点

[孤立节点_无跨实例互动.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/69c3f117-d847-41e6-b241-ac3158b7ce2b)

4）双向节点

[双向节点_既有主动又有被动.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/166b9904-b26f-4a80-a8cf-ad32f11489ae)

综合上述节点分类，给出一个统计信息

[节点类型统计摘要.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/59a1120d-e695-4d4e-bc52-42f97a208c93)

4、使用自然语言处理模型分析实例主题

根据文件“实例_按活跃用户数排序”，使用自然语言处理模型，对每个实例的主题数据进行处理，生成输出文件中的”清理后标签“，随后确定实例主题名称，并给实例进行分类。

最终得到以下文件：

[多语言主题分析完整报告.xlsx](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/2ba50e9f-8664-4be1-b7a6-f92a32eea495)

该文件包含所有实例处理后的主题信息，并根据主题进行归类。

[最常见主题标签.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/b63be33f-fd95-4da3-b91f-65e396cb9a33)

[主题分析摘要.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/005f2c4e-85f2-42da-81a6-aba87545e50f)

[主题聚类统计.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/ea98ed4e-9fb9-41ea-bb14-fe76a633d2ba)

这两个文件对主题分析提供了大略信息。

最后给出主题分析的可视化图表。

![image.png](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/2fba0e0e-40c2-4943-ba97-ccea1a390a62)

下面是该分析的python代码

[deal_theme.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/99d389f1-343b-45ce-a505-cbd36c7d4412)

11.1

根据instance.social爬取实例的语言信息，对于没有显示语言的实例，根据实例描述识别语言。

得到数据集：

[instances_with_detected_language.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/f911b5f8-5e4a-4889-bc03-39571a1ee769)

分析这个数据集，对实例的语言进行分类，得到：

[instances_language_classified.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/6bfa3db8-e037-45b8-b899-b2127fc93ef9)

以下是实现本次分析的python代码

爬取实例语言信息

[instance_language_detected.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/43edc65d-599f-4974-a92b-6955e7d08276)

根据语言对实例分类

[language_classfied.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/57ec07e7-e26c-443d-b8c5-80d26c0de5f2)

11.2

社区检测，使用Louvain算法和标签传播算法分别进行社区检测。

结构中Louvain算法得到的社区模块度更高，意味着找到了更清晰的社区结构。将此结果导出为.csv文件（文件过大传不上来）。

还得到了对应社区分析：

[community_detailed_analysis.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/36182c55-da9b-4d60-a1f0-9f7bceae240e)

以下是实现社区检测的算法：

[community_detect.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/e0aecc7b-9a1c-400a-a336-d84114aa3d25)


