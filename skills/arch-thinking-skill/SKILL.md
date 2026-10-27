---
name: arch-thinking-skill
description: Reconstruct existing software systems from code and maintain architecture understanding across sessions. Use for legacy-code audits with stale docs, page-level PRD and module-level technical design, cross-module debugging, architecture-sensitive changes, and delivery.
---

# Architecture Thinking

从项目 README 定位知识入口，全文读取适用 AGENTS，继承当前任务及已有授权。**接管或上下文压缩后，恢复简洁的 ARCHITECTURE 与 STATE：系统怎样运行、任务要求什么、实现到哪里、下一步依据是什么。** 项目已有同职责文档时沿用实际路径；简单局部编辑只加载相关系统背景。

首次使用时读取[工程思维](assets/workspace/工程思维.md)的核心方法及六条工程判断规则。工作区初始化后，以当地工程思维正文为接续入口；恢复隐含契约、解释模块组合、选择修改边界或修订架构理解时，回读对应方法。**全局模型指导局部追踪，局部证据修正全局模型；设计契约、代码实现与运行事实分别承接。**

按任务目标加载对应方法及其依赖：

| 触发场景 | 读取与交付 |
| --- | --- |
| 全面接管遗留库、从代码反推 PRD／技术设计、要求逐模块说明现状，包括旧文档过期的系统 | 同时读取[系统重建](references/system-reconstruction.md)、[语义追踪](references/flow-tracing.md)和[知识维护](references/knowledge-maintenance.md)；从源码入口建立覆盖清单，逐模块解释产品规则、内部机制和跨模块影响，完成图与正文的走读。工作区知识缺失时再读[初始化](references/initialization.md)。 |
| 用户要求 init，或长期任务缺少可接续的系统知识 | 读取[初始化](references/initialization.md)和[知识维护](references/knowledge-maintenance.md)；当任务同时要求全面重建时，加载上一行的完整依赖。 |
| 按既定设计实施、反馈 Debug、重构、PR 或运维交付 | 读取[任务路由](references/task-routing.md)；遇到多套实现、跨模块状态、异步恢复或实际路径不明时读取[语义追踪](references/flow-tracing.md)。持久系统关系或任务状态改变时读取[知识维护](references/knowledge-maintenance.md)定点回写。 |
| 单独要求架构图、模块图或变更影响解释 | 读取[知识维护](references/knowledge-maintenance.md)，沿相关实际路径读取[语义追踪](references/flow-tracing.md)；覆盖全系统时同时读取[系统重建](references/system-reconstruction.md)。 |

设计来自 chat、文档或 issue 均可，继承已确定的行为、约束和验收。沿真实入口、实现选择、状态读写及消费者恢复现状；用 rg / rg --files 定位线索，随源码证据调整查询。旧文档和规范化外观提供线索，当前行为由实际路径及适用版本确认。局部任务按相关依赖深入；全系统重建按覆盖清单推进。验证针对真实契约和故障机制，文档按唯一职责更新。
