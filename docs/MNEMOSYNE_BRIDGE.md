# 与已安装 Mnemosyne 搭桥

这是一份实现指南，不含 HTTP 请求代码，不会自动连接 Node。不要通过安装此模板声称已经接入。

## 1. 用户提供明确连接资料

用户/宿主提供 base_url、api_prefix、凭证管理器中的引用、组件身份、授权范围和目标 Bank。凭证不放在材料正文、Manifest、源码或公开示例里。

模板不扫描本机端口，不查找 Memory Bank，不读取音乐组件配置，不从其他应用借用管理员 token。已有明确授权配置可直接使用，无须反复索取同一授权。

## 2. 核对真实公开契约

衍生 Bridge 才实现检查。可参考用户安装版本的 OpenAPI/manifest/SDK，并以获授权最小请求验证：

- 健康：参考版本支持 `GET {prefix}/health`；可达不等于获权。
- 观察：参考版本支持 `POST {prefix}/observations`，请求形状来自该版本 ObservationIn。
- 检索：参考版本采用 `POST {prefix}/memories/search`，不是随意猜测 `/search`。
- 权限/组件身份/领域包/认知状态：按该版本实际文档逐项确认；没有则 unsupported 或 unobservable。

这不是对所有 2.0 安装的完整兼容保证。示例基于编写时本地参考契约，不自动推断其他安装具有新增端点。版本字符串不能替代功能核对；也不能从音乐文档里的版本称呼推断用户 Node 版本。

Node 的 `/capabilities` 可能描述治理能力而非完整路由目录，不能仅根据名称推断所有端点存在。404、403、网络故障和合法证据不足分开处理。

## 3. 映射 Observation

`examples/observation.example.json` 是虚构静态形状示例，默认禁止存储，并非可以直接运行的同步命令。

SourceKind 使用实际公开枚举。普通第三方导入在参考契约中可映射 `system`，原平台、来源角色、修订、主体、覆盖和用途限制保存在 metadata；不要发明 `qq`/`bilibili` 顶层 source_kind，也不要批量映射成 user_statement。

Bank 要通过实际支持的授权与路由落实。若 metadata.source_ref.bank_id 只是声明而未执法，不能声称跨 Bank 隔离已成立；不支持时拒绝，不静默写入 personal。

原文/引用与后续解析分开。若先做摘要再入库，摘要标 derived_summary，保留原文引用及实际依赖；不能用生成摘要伪装原始观察。

## 4. 回执与认知阶段

参考版本可能返回 Observation ID、persisted_ok、retrieval_ready、write_stages、auto_verified。只解释明确返回的字段；`INDEXED` 代表可检索，不能写成“已核验”。

衍生组件应持久记录请求幂等键、关联 ID、响应 ID和修订。超时且是否提交未知时，先核对支持的幂等/状态机制；没有则报告 unknown，不盲重发或本地假成功。

之后用 Node 已有的公开接口查看/提出来源依赖的候选、概念、关系与待验证问题。具体核验和采用归 Node。不要创建一套本地长期真相表弥补缺少认知状态接口。

若无可观察的后续认知状态，read_cognition_state 在衍生项目里报告 unobservable，并说明仅确认了写入/索引。模板默认方法仍抛未实现异常。

## 5. 修订、撤回与作用范围

同一来源的 record_id/revision 稳定去重。来源修订或撤回通过 Node 的受控更新/重审流程处理，不能删核心表或把所有下游事实直接清空。

本体注册为可选能力；只声明概念不等于学习了作者观点或写入用户偏好。远程 Node 通常读不到组件所在机器的文件路径，应按公开契约传受支持的 inline 内容，而不是假设共享磁盘。

组件自己的缓存/队列若确有需要，可以在其受控目录设计；永远不把 Node 的 SQLite 作为组件后门。模板没有缓存、队列或任何磁盘数据实现。
