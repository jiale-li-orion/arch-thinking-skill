---
name: arch-thinking-skill
description: Understand, implement, and evolve software systems across sessions. Use for approved-design implementation, feature work, cross-module debugging, legacy-system changes, refactoring, PR and operational delivery, and maintaining useful workspace architecture memory.
---

# Architecture Thinking

从项目 README 定位知识入口，全文读取适用 AGENTS，继承当前任务及已有授权。**接管或上下文压缩后，恢复简洁的 ARCHITECTURE 与 STATE：系统怎样运行、任务要求什么、实现到哪里、下一步依据是什么。** 项目已有同职责文档时沿用实际路径；简单局部编辑只加载相关系统背景。

首次使用时读取[工程思维](assets/workspace/工程思维.md)的核心方法及六条工程判断规则。工作区初始化后，以当地工程思维正文为接续入口；恢复隐含契约、解释模块组合、选择修改边界或修订架构理解时，回读对应方法。**全局模型指导局部追踪，局部证据修正全局模型；设计契约、代码实现与运行事实分别承接。**

按[任务路由](references/task-routing.md)选择当前策略：按设计实施、反馈 Debug、重构演进或交付运维。再根据系统掌握程度补充调查；大型遗留库、多套实现或兼容关系复杂时，加载其中的遗留系统策略。设计来自 chat、文档或 issue 均可，继承已确定的行为、约束和验收。

代码搜索需要调整线索与覆盖范围，或跨模块、跨进程、异步、持久化、状态归属影响判断时，读取[语义追踪](references/flow-tracing.md)的对应章节。用 rg / rg --files 定位入口，随源码证据更新查询；从调用使用和状态变化恢复隐含契约，沿机制链区分原因解释，判断证据对修改边界的支持。验证遵循工程思维中的原始规则，针对真实契约和故障机制。

用户要求 init，或长期维护、跨模块任务缺少可接续的系统知识时，读取[初始化](references/initialization.md)：补齐必要结构，继续从设计、代码、配置与反馈恢复真实知识，完成可接续正文。一次性局部任务直接依据现有项目资料和源码推进，文档沉淀取决于后续复用价值。知识体系就绪后直接推进当前任务。

需要向人呈现系统现状与修改影响，或系统关系、判断前提、任务状态改变时，按[知识维护](references/knowledge-maintenance.md)构建带条件与证据的系统、模块及行为视图，更新唯一负责的正文。复用已有工作区文件与 Git；脚本只辅助建文件、定位引用和检查证据路径。
