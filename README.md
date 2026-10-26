# arch-thinking-skill

面向长期维护的 Coding 工作区：让 Agent 先恢复工作区知识，再根据任务阶段选择操作策略，并把值得复用的新认知更新回工作区。记忆归工作区所有；Skill 只定义建立、读取、更新和核验这些资产的机制。

## 图 1：Skill 自身的模块与依赖

~~~mermaid
flowchart TB
    INDEX["README.md<br/>架构索引与依赖图"]
    RULES["AGENTS.md<br/>Skill 结构维护协议"]
    SKILL["SKILL.md<br/>入口、公共机制、渐进式路由"]
    ROUTE["references/task-routing.md<br/>实施 / Debug / 旧系统 / 交付"]
    FLOW["references/flow-tracing.md<br/>代码语义、调用链、状态与失败"]
    MEMORY["references/workspace-memory.md<br/>工作区知识架构与依赖"]
    MAINT["references/memory-maintenance.md<br/>知识更新、回读、失效、裁剪"]
    TOOL["scripts/arch_memory.py<br/>init / impact / check"]
    TEST["tests/<br/>工具的关键行为生命周期"]

    INDEX --> SKILL
    RULES --> SKILL
    SKILL --> ROUTE
    SKILL -. "when tracing a cross-module flow" .-> FLOW
    SKILL -. "when setting up workspace memory" .-> MEMORY
    SKILL -. "when maintaining knowledge" .-> MAINT
    MEMORY --> TOOL
    MAINT --> TOOL
    TOOL --> TEST
~~~

入口只负责识别任务阶段、恢复相关知识和选择下一步。详细操作策略按需加载；工具只自动化可机械判定的工作，不代替 Agent 对代码语义和架构的判断。

## 图 2：每个 Coding 工作区的知识依赖

~~~mermaid
flowchart TB
    INPUT["外部任务契约<br/>Chat 中已批准的 PRD / Tech Design"]
    SOURCE["代码证据<br/>源码 / 配置 / API / Git 历史 / 运行反馈"]
    ENTRY["README.md<br/>知识索引、依赖图、任务回读路由"]
    RULES["AGENTS.md<br/>稳定维护协议、回读条件、更新责任"]
    ARCH["ARCHITECTURE.md<br/>全局系统模型与不变量"]
    STATE["STATE.md<br/>当前认识、未决问题、下一步调查"]
    FLOW["flows/<name>.md<br/>必要时维护的局部业务链路"]
    RUN["任务 / PR / 运维记录<br/>本次执行与交付事实"]

    INPUT --> ENTRY
    SOURCE --> ARCH
    SOURCE --> FLOW
    ENTRY --> RULES
    RULES --> ARCH
    RULES --> STATE
    ARCH <--> STATE
    ARCH <--> FLOW
    FLOW -. "when local evidence changes global understanding" .-> STATE
    RUN -. "reusable findings only" .-> STATE
~~~

箭头表示知识来源、读取依赖和认知反馈，不是每次任务必须执行的线性步骤。设计契约描述预期行为，源码和运行证据描述实际行为；两者有差异时保留差异并调查，不让任何一方悄悄覆盖另一方。

## 文件职责

| 文件 / 目录 | 唯一职责 | 何时读取 |
|---|---|---|
| SKILL.md | Skill 入口、公共认知循环、任务路由与渐进加载 | 任务命中 Skill 时 |
| AGENTS.md | 本仓库的文档职责、依赖维护与修改约束 | 修改 Skill 结构或内容时 |
| references/task-routing.md | 根据产品/实现阶段选择实施、Debug、旧系统探索或交付策略 | 任务阶段判定后 |
| references/flow-tracing.md | 从源码语义恢复端到端行为、状态所有权和失败路径 | 跨模块行为或故障需要解释时 |
| references/workspace-memory.md | 设计工作区知识资产的依赖、全局/局部关系和渐进式加载 | 初始化或调整工作区知识架构时 |
| references/memory-maintenance.md | 定义知识更新、失效、回读与裁剪机制 | 修改或维护知识资产时 |
| scripts/arch_memory.py | 初始化知识骨架、按源码变更定位引用笔记、检查证据引用 | 需要机械化检查时 |
| tests/ | 验证工具的关键行为链路，不衡量 Skill 内容的质量 | 修改工具行为后 |

## Coding 任务路由

- **设计已定稿 → 实施：** 将用户提供的设计和验收标准作为契约，映射到现有代码，实施并核验。
- **实现反馈 / Bug：** 比较预期与实际，追踪最早偏差、状态与失败恢复，针对机制修复。
- **旧系统 / 意图不清：** 通过 rg / grep 和源码语义逐步恢复相关系统模型。
- **PR / 运维交付：** 按现有仓库流程核验变更、交付状态和回滚约束。

任务路由是可切换的状态，不是固定流水线。实施中发现设计缺口可以回到澄清；Debug 发现系统模型缺失可以局部探索；交付后的反馈重新进入 Debug。

## 设计约束

- 工作区知识是唯一的长期记忆载体；不依赖 Agent 隐式长期记忆。
- 大型 Coding Repo 可使用独立的小型 Git 知识仓库；小项目也可使用源码仓库内的 .arch/。
- 先追踪代码语义，再决定是否需要测试；测试应覆盖真实模块边界和有意义的行为。
- 只在知识影响未来搜索、解释、决策或验证时更新文档；不为每个任务生成总结。
- 不默认生成全仓库图谱、向量库、重复 PRD 或多余索引。

## 状态

当前为架构骨架阶段。文档职责、依赖和任务路由先稳定；各模块的具体方法与细节由后续设计逐步填充。
