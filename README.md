# arch-thinking-skill

面向软件系统的理解、实现与演进。全局架构指导局部语义追踪，代码和运行反馈修正系统模型；阶段策略完成当前任务，工作区文档使理解能够持续接续。

适用于按批准设计实施、功能迭代、Debug、重构、PR 和运维。大型遗留库是其中一个深入场景：需要辨认多套实现、恢复隐含契约、平衡复用与新逻辑并把握修复边界。

## 安装到 Codex

本仓库同时提供 [Codex 插件包](.codex-plugin/plugin.json)和可单独安装的 [Agent Skill](skills/arch-thinking-skill/SKILL.md)。安装插件：

```bash
codex plugin marketplace add jiale-li-orion/arch-thinking-skill
codex plugin add arch-thinking-skill@arch-thinking-skill-marketplace
```

只安装 Skill 时，在 Codex 中使用 `$skill-installer`，指定 `https://github.com/jiale-li-orion/arch-thinking-skill/tree/main/skills/arch-thinking-skill`。本地开发可将 `skills/arch-thinking-skill/` 链接到 `~/.codex/skills/arch-thinking-skill/`。安装后重启 Codex，让新会话发现 Skill。仓库根目录的 README 与 AGENTS 面向维护者；安装内容位于 `skills/arch-thinking-skill/`，工作区初始化按下文脚本及当地系统资料完成。

许可见 [MIT License](LICENSE)。仓库发布内容由 Git 跟踪；本地归档按当地 `.gitignore` 排除。

## 渐进加载与职责

| 入口 | 职责与加载条件 |
| --- | --- |
| [SKILL](skills/arch-thinking-skill/SKILL.md) | 接管、公共方法和按需路由 |
| [AGENTS](AGENTS.md) | 维护本 skill 的职责与原始规则 |
| [工程思维](skills/arch-thinking-skill/assets/workspace/工程思维.md) | 从隐含契约、组合解释与归因推导修改边界的完整方法；初始化后由工作区持有 |
| [任务路由](skills/arch-thinking-skill/references/task-routing.md) | 按任务阶段选择交付策略，按理解缺口切换全局分析、局部取证与实施 |
| [语义追踪](skills/arch-thinking-skill/references/flow-tracing.md) | 真实路径、契约恢复、因果链与竞争解释取证 |
| [初始化](skills/arch-thinking-skill/references/initialization.md) | 接入已有文档，补齐结构并恢复真实系统知识 |
| [知识维护](skills/arch-thinking-skill/references/knowledge-maintenance.md) | 面向人类决策的现状图、证据与覆盖、判断前提回传及保真接续 |
| [工作区模板](skills/arch-thinking-skill/assets/workspace/README.md) | README、AGENTS、工程思维、ARCHITECTURE、STATE；按实际缺口使用 |
| [辅助脚本](skills/arch-thinking-skill/scripts/arch_memory.py) | init / impact / check；只执行机械辅助 |

工程正文保存在工作区，设计可以来自 chat、文档或 issue。现有同职责资产直接继承，源码和 Git 提供具体证据与历史。默认使用工作区内普通文件，复杂模块和链路按需展开。

## 图 1：Skill 与工作区如何衔接

```mermaid
flowchart TB
    SK[SKILL 接管与路由] --> EN[项目 README 与 AGENTS]
    EN --> AR[ARCHITECTURE 简洁全局]
    EN --> ST[STATE 契约与任务]
    SK --> TH[工程思维 通用判断]
    SK --> RT[任务路由 按阶段选择]
    RT --> TR[语义追踪 按需深入]
    SK --> IN[初始化 结构与知识恢复]
    IN --> TM[工作区模板]
    TM --> EN
    IN --> AR
    IN --> ST
    AR <--> FL[模块与行为视图 条件与证据]
    ST --> FL
    TR --> FL
    SK --> KM[知识维护]
    KM --> AR
    KM --> ST
    KM --> FL
```

方法、策略、项目知识和机械工具分别维护。入口保持短，所需细节沿实际任务加载。

## 图 2：行动与理解共同迭代

```mermaid
flowchart TD
    START[接管或上下文恢复] --> READ[入口 规则 全局架构 当前状态]
    READ --> READY{接续知识的就绪状态}
    READY -->|需要补充| INIT[恢复设计 源码 配置与运行事实]
    INIT --> READ
    READY -->|能够行动| TASK[选择任务策略与相关系统条件]
    TASK --> GLOBAL[定位职责 状态归属 实现选择及约束]
    GLOBAL --> LOCAL[rg 定位与局部语义追踪]
    LOCAL --> IMPACT[恢复契约 机制归因 判断修改边界]
    IMPACT -->|分歧影响修改选择| LOCAL
    IMPACT --> CHANGE[完成最小完整修改]
    CHANGE --> VERIFY[依据契约与机制选择有效验证]
    VERIFY -->|反馈需要解释| LOCAL
    VERIFY -->|满足验收| DELIVER[完成授权范围内交付]
    LOCAL -->|关系或判断前提变化| UPDATE[更新全局与局部视图 依据及影响]
    UPDATE --> GLOBAL
    DELIVER --> STATE[更新当前接续与实际交付状态]
```

调查与实施可以往返，文档更新由有价值的关系变化触发。新系统沿设计建立实现；成熟系统按任务复用；遗留库在实际路径与兼容关系清楚后确定修改范围。

## 初始化与接续

用户明确要求初始化，或长期维护、跨模块任务缺少可接续的系统知识时，读取[初始化流程](skills/arch-thinking-skill/references/initialization.md)。脚本补缺文件，Agent 继续填写真实系统图、任务契约、实现差距、证据和下一动作：

```bash
python3 skills/arch-thinking-skill/scripts/arch_memory.py init --root /path/to/repo
```

已有其他文档位置时指定 `--memory-root`。旧版 `.arch/` 的接续规则见初始化流程。图谱服务与检索插件属于可选外部能力；本 skill 的完整工作路径使用文档、rg、源码、Git 和必要的运行证据。

## 方法边界

系统理解由真实契约、生产消费、存储计算通信、状态生命周期、复用与交付共同约束。长期知识归并保留后续需求、故障与迁移仍会用到的机制区别；当前任务的过程由任务记录和 Git 承接。六条工程判断规则保存在[工程思维](skills/arch-thinking-skill/assets/workspace/工程思维.md#六条工程判断规则原文保留)。

相关机制参照：[Go pipelines](https://go.dev/blog/pipelines)解释生产者退出与资源释放；[Tokio channels](https://tokio.rs/tokio/tutorial/channels)区分交接与完成；[Google code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)结合整体设计、真实行为和变更上下文审查。具体项目按其语言、运行时和接口语义应用。
