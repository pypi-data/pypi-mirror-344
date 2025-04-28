"""
版本管理模块，处理代码生成的版本控制、历史追踪和回退功能。

该模块提供了以下功能:
1. 提取历史轮次的日志信息
2. 格式化历史执行记录用于AI参考
3. 分析用户需求，决定是否需要版本回退
4. 执行Git版本回退操作
5. 为AI助手提供版本回退工具
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional

from langchain_core.tools import Tool, StructuredTool
from pydantic import BaseModel, Field

from core.ai import AIConfig, AIAssistant
from core.diff import DiffInfo
from core.git_manager import GitManager
from core.log_config import get_logger
from core.log_manager import LogManager
from core.prompt_generator import PromptGenerator

logger = get_logger(__name__)

@dataclass
class VersionInfo:
    """存储特定版本的信息"""
    issue_id: int
    round_num: int 
    requirement: str
    agent_response: str
    modified_files: List[DiffInfo] = None


class VersionManager:
    """管理代码生成的版本信息，支持版本回退和需求整合"""

    def __init__(self, issue_id : int, ai_config: AIConfig, log_manager: LogManager, git_manager: GitManager):
        """
        初始化版本管理器
        
        Args:
            log_manager: 日志管理器实例
            git_manager: Git管理器实例
        """
        self.ai_assistant = AIAssistant(config=ai_config, tools=[self._create_version_manager_tool()])
        self.log_manager = log_manager
        self.git_manager = git_manager
        self.current_issue_id = issue_id
        self.current_round_num = log_manager.get_current_round()
        self.issue_branch = f"bella-issues-bot-{issue_id}"

    def ensure_version_and_generate_context(self, original_requirement: str) -> tuple[str, str]:
        rollback = False,
        requirement = None
        reasoning = None
        if self.current_round_num > 1 :
            rollback, rollback_num, requirement, reasoning = self._analyze_rollback_need(original_requirement)
        requirement = original_requirement if requirement is None else requirement
        history = self.get_formatted_history(rollback, reasoning)
        return requirement, history

    def init_environment(self, mode: str) -> str:
        """
        根据模式初始化工作环境，包括分支操作
        
        Args:
            mode: 运行模式，"client" 或 "bot"
            
        Returns:
            str: 当前使用的分支名称
        """
        if mode == "bot":
            # 在bot模式下，需要切换到issue对应的分支
            # 获取当前分支
            try:
                self.git_manager.reset_to_issue_branch(self.current_issue_id)
                logger.info(f"Bot模式: 已重置到issue #{self.current_issue_id}的分支: {self.issue_branch}")
            except Exception as e:
                logger.error(f"初始化issue分支失败: {str(e)}")
                # 如果失败，尝试创建分支
                try:
                    self.git_manager.switch_branch(self.issue_branch, create=True)
                    logger.info(f"已创建并切换到分支: {self.issue_branch}")
                except Exception as e:
                    logger.error(f"创建分支失败: {str(e)}")
        
        return self.issue_branch

    def _extract_history(self) -> List[VersionInfo]:
        """
        提取当前issue的历史版本信息
            
        Returns:
            List[VersionInfo]: 历史版本信息列表
        """
        # 获取所有轮次的日志条目
        log_entries = self.log_manager.get_issue_log_entries()
        
        # 提取每轮的需求和响应
        version_info_list = []
        for entry in log_entries:
            try:
                # 从用户提示中提取需求
                extracted_info = PromptGenerator.extractInfo(entry.prompt)
                requirement = extracted_info.requirement
                
                # 创建版本信息
                version_info = VersionInfo(
                    issue_id=self.current_issue_id,
                    round_num=entry.round_num,
                    requirement=requirement,
                    agent_response=entry.response,
                    modified_files=entry.modified_files
                )
                version_info_list.append(version_info)
                
            except Exception as e:
                logger.error(f"提取轮次 {entry.round_num} 的信息时出错: {str(e)}")
        
        return version_info_list

    def get_formatted_history(self,
                              rollback: bool = False,
                              reasoning: Optional[str] = None) -> str:
        """
        获取格式化的历史执行记录
        
        Args:
            
        Returns:
            str: 格式化的历史执行记录
        """
        history = self._extract_history()
        formatted_history = []
        
        for version in history:
            formatted_history.append(f"【round_{version.round_num}】")
            formatted_history.append(f"requirement: \n{version.requirement}")
            
            # 简化AI响应，避免历史记录过长
            formatted_history.append(f"agent_response: \n{version.agent_response}")
            formatted_history.append("")  # 添加空行分隔
        formatted_history.append("=========================以上【历史执行记录】内容为历史执行过程，所有代码改动均已经生效========================================")
        if rollback:
            formatted_history.append("=========================经过分析后续的历史执行过程不符合用户需求，已经回滚，不在此展示============================")
            if reasoning:
                formatted_history.append(f"回滚原因:\n{reasoning}")
        return "\n".join(formatted_history)

    def _analyze_rollback_need(self,
                              current_requirement: str) -> Tuple[bool, Optional[int], Optional[str], Optional[str]]:
        """
        分析是否需要版本回退
        
        Args:
            current_requirement: 当前用户需求
            
        Returns:
            Tuple[bool, int, str, str]: (是否需要回退, 回退到的轮次, 整合后的需求，决策的原因)
        """
        # 获取历史记录
        history = self.get_formatted_history()
        
        # 构建提示词
        prompt = f"""
# 角色
你是一位资深程序员，现在在处理用户的issues，请分析本次用户提出的需求和历史执行记录，判断之前提交的代码是否需要版本回退。并调用工具完成版本的创建。

# 历史执行记录
{history}

# 当前用户需求
{current_requirement}


#执行步骤
##工具参数分析
你需要调用 version_manager 工具来处理问题，请请根据上述信息分析以下问题，
1. 是否需要回退到某个特定版本? 如果需要，则调用工具时的参数 need_rollback 为 True
2. 如果需要回退，应该回退到哪个round?  调用工具时的参数，如果全部回退则为0。
3. 如果需要回退，当前需求的信息是否完整？需要把回退到的round之后的round需求与当前需求结合，作为补充信息吗? 如果需要结合，则将重写后的本轮需求，作为integrated_requirement参数；如果不需要则不需要此参数。
4. 做出这个决策的原因是什么？调用工具时，作为reasoning参数

##工具执行
根据得到的参数，调用version_manager。无论是否需要rollback必须调用工具执行任务，完成当前版本的创建。

"""

        # 发送给AI进行分析
        response = self.ai_assistant.generate_response(prompt, use_tools=True)

        # 默认返回值
        default_return = (False, 0, current_requirement, None)
        
        # 如果响应是元组，说明工具已执行并返回了结果
        if isinstance(response, tuple) and len(response) >= 4:
            return response
        
        # 返回默认值
        return default_return

    def _rollback_to_version(self, target_round: int) -> bool:
        """
        执行基于文件的版本回退

        首先回滚日志，然后回滚文件改动
        
        Args:
            target_round: 目标轮次
            
        Returns:
            bool: 回退是否成功
        """
        try:
            # 首先执行日志回滚
            log_rollback_success = self.log_manager.rollback_log(target_round)
            if not log_rollback_success:
                logger.warning(f"日志回滚失败，但将继续执行文件回滚")

            # 获取目标轮次的日志条目
            log_entries = self.log_manager.get_issue_log_entries(include_diff=True)
            
            if not log_entries:
                logger.error("找不到任何日志条目")
                return False
            
            # 获取当前轮次到目标轮次之间的所有轮次记录，按轮次降序排列（从最新到最旧）
            entries_to_rollback = sorted(
                [entry for entry in log_entries if entry.round_num > target_round],
                key=lambda entry: entry.round_num,
                reverse=True
            )
            
            if not entries_to_rollback:
                logger.info(f"当前已经是轮次 {target_round} 或更早，无需回滚")
                return True
            
            # 依次回滚每一轮的修改
            import os
            project_dir = self.log_manager.config.project_dir
            
            for entry in entries_to_rollback:
                logger.info(f"正在回滚轮次 {entry.round_num} 的修改...")
                
                if not entry.modified_files:
                    logger.info(f"轮次 {entry.round_num} 没有文件修改，跳过")
                    continue
                
                # 对每个修改的文件进行回滚
                for diff_info in entry.modified_files:
                    file_path = os.path.join(project_dir, diff_info.file_name)
                    
                    if diff_info.is_create:
                        # 如果是创建操作，则删除该文件
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            logger.info(f"删除文件 {diff_info.file_name}，回滚轮次 {entry.round_num} 的创建操作")
                    
                    elif diff_info.is_modify:
                        # 如果是修改操作，则恢复到修改前的内容
                        if diff_info.file_content is not None:
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(diff_info.file_content)
                            logger.info(f"恢复文件 {diff_info.file_name} 到轮次 {entry.round_num} 修改前的状态")
                        else:
                            logger.warning(f"文件 {diff_info.file_name} 没有保存修改前的内容，无法回滚")
                    
                    elif diff_info.is_delete:
                        # 如果是删除操作，则恢复文件
                        if diff_info.file_content is not None:
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(diff_info.file_content)
                            logger.info(f"恢复文件 {diff_info.file_name}，回滚轮次 {entry.round_num} 的删除操作")
                        else:
                            logger.warning(f"文件 {diff_info.file_name} 没有保存删除前的内容，无法回滚")
            
            logger.info(f"成功回滚到轮次 {target_round}")
            return True
            
        except Exception as e:
            logger.error(f"文件版本回退失败: {str(e)}")
            return False

    class _VersionManagerToolSchema(BaseModel):
        need_rollback: bool = Field(
            ...,
            examples=[True, False],
            description="是否需要回退版本"
        )
        target_round: Optional[int] = Field(
            None,
            examples=[0,1,2,3,4],
            description="要回滚到的目标轮次，只有need_rollback为True时需要且必须。全部回退值为0"
        )
        integrated_requirement: Optional[str] = Field(
            None,
            description="整合后的需求，只有need_rollback为True且需要重写需求时需要"
        )
        reasoning: Optional[str] = Field(
            None,
            description="做这个出决策的原因"
        )

    def _create_version_manager_tool(self) -> StructuredTool:
        """
        版本管理工具，供AI助手使用
            
        Returns:
            Tool: 版本管理工具
        """
        def version_manager_tool(need_rollback: bool,
                                          target_round: Optional[int] = None,
                                          integrated_requirement: Optional[str] = None,
                                          reasoning: Optional[str] = None) -> Tuple[str, Optional[int], Optional[str], Optional[str]]:
            """
            决定是否回退版本并执行回退
            
            Args:
                need_rollback:是否需要回退,
                target_round：回退到的轮次,
                integrated_requirement： 整合后的需求
                reasoning: 做出决策的原因
                
            Returns:
                str: 执行结果
            """
            
            if need_rollback and target_round is not None:
                success = self._rollback_to_version(target_round)
                if(success) :
                    return (True, target_round, integrated_requirement, reasoning)
                else:
                    logger.warning(f"版本回退失败:issues:{self.current_issue_id},target:{target_round},integrated_requirement:{integrated_requirement}")
            return (False, 0, None, reasoning)
        
        return StructuredTool.from_function(
            name="version_rollback_manager",
            description="用于决定当前项目版本的工具，如果 need_rollback 为True，则根据target_round和integrated_requirement进行版本回退；如果need_rollback为False则保持当前版本",
            func=version_manager_tool,
            return_direct=True,
            args_schema=self._VersionManagerToolSchema
        )

    def apply_changes(self, mode: str, response: str, is_code_change: bool = True) -> bool:
        """
        根据模式提交和推送更改
        
        Args:
            mode: 运行模式，"client" 或 "bot"
            response: 回复
            is_code_change: 是否是代码修改（影响提交信息）
            
        Returns:
            bool: 操作是否成功
        """
        if mode != "bot":
            logger.info("客户端模式: 跳过提交和推送")
            return True
            
        try:
            # 构建提交信息
            commit_type = "generate" if is_code_change else "chat"
            commit_message = f"issues#{self.current_issue_id}-{commit_type} by Bella-Issues-Bot"
            
            # 提交更改
            self.git_manager.commit(commit_message)
            logger.info(f"已提交更改: {commit_message}")
            
            # 推送到远程仓库
            if self.git_manager.config.remote_url:
                self.git_manager.push(branch=self.issue_branch, force=True)
                logger.info(f"已推送更改到分支: {self.issue_branch}")
                self.git_manager.add_issue_comment(self.current_issue_id, response)
                
            return True
        except Exception as e:
            logger.error(f"提交或推送更改失败: {str(e)}")
            return False
