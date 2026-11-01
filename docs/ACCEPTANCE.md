# 两种验收，分别报告

## A. 模板本体

使用 `python -B -m unittest discover -s tests -v`，不需要访问账号、Node 或 Memory Bank。

验证：

- 包无运行时依赖、CLI、服务或自动启动入口。
- 所有来源/标准化/桥接/研究扩展方法均抛出 TemplateNotImplementedError。
- 代码没有网络、文件采集、凭证访问、数据库或平台 SDK 实现；导入只加载类型和桩。
- 示例 Manifest 不叫可自动发现的 mnemosyne.component.json，provides/permissions/banks 为空。
- 配置未实施、自动获取关闭，连接和授权未配置。
- 静态记录为虚构数据，来源与认知阶段保持区分，文档链接完整。

这些测试通过只证明模板的结构和无能力边界，不证明真实采集或 Mnemosyne 接入成功。

## B. 用户衍生的实际组件

开发后需要另外实现和运行：

1. 授权前不读取来源；范围撤销后立即停止；已安装不等于获权。
2. 原始记录、主体、时间、覆盖、来源角色和版本可追溯；作者观点不变用户立场。
3. 同记录同修订重放幂等，新修订可识别；部分列表缺失不触发删除。
4. 明确 Node 与 Bank，接口缺失/403/404/网络故障分别解释；不默认回落个人 Bank。
5. 实际 Observation 回执可核对；超时未知不假成功或盲重试。
6. 入库/索引/候选/核验分开；没有后续状态接口就 unobservable。
7. 源撤回/修改会让受影响派生物重审；不得绕过 Node 直接改数据库。
8. 真正实现研究扩展时覆盖 RESEARCH_POLICY.md 的阈值、权限、隐私、预算、重复及停止用例。
9. 使用隔离 fake source/fake Node 验证错误和流程，再用临时 Bank 验证真实公开契约。测试中的临时 fake 不是交付时的“成功”后门。
10. 在明确授权的最小真实来源上记录平台/Node 版本、接口、范围、结果与限制；没测的平台不宣布支持。

交付报告分别列：implemented、tested_with_fixture、tested_with_temporary_node、tested_with_real_authorized_source、unimplemented。不得把这些状态合并成一个 ready=true。

## C. 开源交付

保留许可证，记录修改，公开接口、范围、安装/卸载和测试方法。不提交个人导出、凭证、生产数据库或隐藏 telemetry；真实抓取样本以经授权脱敏夹具替代。
