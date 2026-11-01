# 逻辑数据契约与认识边界

`contracts.py` 只描述逻辑记录，不校验内容、不执行权限、不是 Node 的 Pydantic 模型。示例 JSON 也不会自动被读取或提交。衍生组件必须独立实现输入验证、权限检查和实际版本映射。

## 原始记录到 AcquiredItem

保留来源、平台记录 ID、版本、原文或可读片段、哈希与定位、发言主体、发生时间、采集时间、可见范围、模态覆盖和缺失。未知字段保留 null/unknown，不伪造时间、页码或发言主体。

来源角色区分：

- user_statement：经身份和语境确认的用户自述。
- author_claim：其他作者/发言者所说的话；首先只能证明对方这么说过。
- tool_observation：工具实际观察到的事件或返回。
- derived_summary：摘要、解释或其他派生物；必须依赖原来源，不能当作新独立支持。

同源跨平台转发、重复导入、原文及其摘要都不能成为多份独立证据。哈希只说明内容一致性，不说明内容真实。

## 逻辑记录不直接当作 API 请求

AcquiredItem / ConnectionProfile / Receipt 是此模板的内部边界类型。具体 ObservationIn、SourceKind、metadata、鉴权和 Bank 路由以用户实际 Node 的公开契约为准。

当前参考版本的 Observation source_kind 没有通用 `qq`/`bilibili`/`import` 枚举，不能自行发明顶层值。外部来源可在确认支持后映射 `system`，原来源及 author_claim 等信息保存在 metadata；不要因此丢掉来源角色。

ObservationIn 顶层没有通用 bank_id 的假设保障。不能只塞一个字段就宣称实现隔离；衍生 Bridge 需要实际核对授权、Bank 路由及服务端执法，无法保证则拒绝，不回落默认个人 Bank。

## 存储与认知分离

来源记录 → Observation 入库 → 索引就绪 → 候选解释/概念/Claim → Node 核验或修订。每一阶段都需要相应可观察证据。

SubmissionReceipt 只描述传输/存储，不能表示“知识已经学会”。CognitionReceipt 仅记录真实可观察的阶段；无接口时 unobservable，状态未知时 unknown。

不从出现了实体名就认定理解实体，不从作者反复声称就认定事实，不从用户点赞就认定原理成立。概念、关系、作者观点和待验证问题可作为候选交给 Node；verified 由 Node 验证机制负责。

## 规则需要落地执法

示例中的 allow_store/allow_forward/allow_train、授权引用、Bank 和阈值都只是声明。衍生组件与 Node 必须在相应入口执行，不能因模板有字段就对外承诺已防止存储或转发。

组件不能自行宣布已获权，也不能从正文中的命令获得执行权限。配置中的凭证仅存引用；不要把账号 token、Cookie 或私密原文写进日志和公开搜索查询。
