# Mnemosyne Acquisition Component Template

**Mnemosyne 生态下的通用信息获取与桥接开发模板。MIT 开源，零运行时依赖。**

帮助用户或 Agent 为尚未被已有组件覆盖的信息来源，开发自己的采集组件，并搭建通向已安装 Mnemosyne 的桥梁。

**这是没有业务能力的模板。** 不含 QQ、B 站、音乐或其他平台采集器；不联网、不搜索、不登录、不读取配置或凭证、不自动发现 Node、不入库、不运行认知处理。所有扩展方法直接抛出 `TemplateNotImplementedError`。安装 Python 包也不会启动任何功能。

本仓库提供的是：接口骨架、数据形状、静态示例、开发流程、信息获取阈值规范，以及验证模板保持无能力的测试。示例不是真实数据，策略字段没有运行时执法实现。

## 分类与定位

- **生态位置**：Mnemosyne → Acquisition Component → 开发模板（不是运行时组件）。
- **组件类型**：Python 包 / 源码模板；无 CLI、无服务、无插件入口、无后台任务。
- **适用场景**：为尚未覆盖的信息来源开发采集与桥接组件，例如用户导出文件、已授权 API、Webhook、公开文档或网页资料。
- **明确不属于**：QQ / B 站 / 音乐等具体平台采集器；长期记忆库；认知引擎；自动联网搜索器。
- **成熟度**：`0.1.0` 模板；只证明“模板保持无能力”和接口边界，不证明任何平台已适配。
- **许可**：MIT。

## 给用户：怎么用

1. 复制本目录到你自己的新组件项目，先改包名、组件 ID 和来源名称。原模板保持无能力，实际实现放在衍生项目。
2. 写明“要获取什么、从哪里、用户允许哪些范围、目标 Node 和 Bank”。尚未提供这些信息时，Agent 先补需求，不扫描账号、端口或私人文件。
3. 让 Agent 读取 [AGENT_BUILD_GUIDE.md](docs/AGENT_BUILD_GUIDE.md)，也可直接粘贴 [开发提示词](docs/AGENT_PROMPT.md)。
4. 先用虚构夹具实现一个来源的最小链路，再通过用户授权范围内的真实测试接入自己的 Node。
5. 通过 [验收清单](docs/ACCEPTANCE.md) 后，衍生组件才声明实际具备的能力。

适用来源不限平台：用户导出文件、已授权 API、Webhook、公开文档、网页资料或其他用户明确提供的输入。QQ、B 站只是待开发来源的例子，模板不声称已支持。

## 给 Agent：实现顺序

需求与范围 → 来源契约 → 来源读取 → 标准化 → Node 契约确认 → 观察入库回执 → 可观测的认知状态 → 故障、撤回与重复处理。

读取、标准化、桥接与补充信息策略分别有扩展点；没有内置编排器、HTTP 客户端、队列、数据库或自动任务。

优先复用用户已经安装、且明确覆盖需求的组件，不重复实现已有音乐组件。不要把音乐业务、播放控制或平台登录复制到通用模板中。

## 目录与阅读入口

- [来源开发指南](docs/SOURCE_DEVELOPMENT.md)：如何选择采集方式、声明覆盖和授权范围。
- [数据与认知契约](docs/DATA_CONTRACT.md)：原始材料、作者观点、推断、证据和认识状态的区别。
- [Mnemosyne 桥接指南](docs/MNEMOSYNE_BRIDGE.md)：对接实际安装版本，避免直接写数据库和虚构接口。
- [补充信息阈值](docs/RESEARCH_POLICY.md)：什么时候建议联网、阻止条件、预算和停止规则；仅规范，未实现。
- [模板测试与衍生组件验收](docs/ACCEPTANCE.md)：分别证明“模板无能力”和“你实现的组件可用”。
- `src/mnemosyne_acquisition_template/`：数据类型、抽象端口和显式失败的桩。
- `examples/`：不自动加载的静态示例；Manifest 特意命名为 `.example.json`，不作为可安装运行组件发布。

## 只验证模板，不连接任何服务

需要 Python 3.10+，无须安装测试依赖：

```bash
python -B -m unittest discover -s tests -v
```

测试覆盖：扩展方法全部拒绝执行、无启动入口、无业务依赖、无网络/数据库实现、示例与文档互相对应。此结果不证明任何平台采集或真实 Node 桥接已经实现。

本次实际执行和验证边界见 [VALIDATION.md](docs/VALIDATION.md)。开发模板请使用整个源码目录或源码压缩包；wheel 仅包含无能力的类型与桩，不替代完整开发指南。

开发时可以将包安装到自己的隔离环境；包没有 CLI、后台进程或服务入口。没有“启动模板”命令，也没有自动授权或自动同步命令。

## 开源与生态关系

本模板的原创代码与文档按 [MIT](LICENSE) 发布，不含闭源依赖或遥测。参考 [mnemosyne-music-acquisition](https://github.com/canyueY/mnemosyne-music-acquisition) 中来源适配与公共 Service Contract 分离的方向；未复制其采集实现，也不要求安装音乐组件。

Mnemosyne Node 负责认知权威，Memory Bank 是其数据目录。模板不会创建第二套长期记忆或将安装视为授权。

## 仓库与下载

- GitHub：[canyueY/mnemosyne-acquisition-component-template](https://github.com/canyueY/mnemosyne-acquisition-component-template)
- 源码模板 zip：[Releases](https://github.com/canyueY/mnemosyne-acquisition-component-template/releases) 中的 `mnemosyne-acquisition-component-template-0.1.0-template.zip`
- 开发指令：直接使用 [docs/AGENT_PROMPT.md](docs/AGENT_PROMPT.md)

本仓库只发布模板与文档；不会替你创建衍生组件或远程项目。
