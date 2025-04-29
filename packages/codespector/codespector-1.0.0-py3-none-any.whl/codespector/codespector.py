from codespector.base import BasePipe
from codespector.local import CodeSpectorDataPreparer
from codespector.reviewer import CodeSpectorReviewer
from codespector.types import AgentInfo


class CodeSpector:
    def __init__(
        self,
        chat_token: str,
        chat_agent: str,
        compare_branch: str,
        system_content: str,
        prompt_content: str,
        data_preparer: CodeSpectorDataPreparer,
        reviewer: CodeSpectorReviewer,
        pipeline: list[BasePipe],
        result_file: str,
        output_dir: str,
        chat_model: str | None = None,
        exclude_file_ext: list[str] | None = None,
    ):
        self.chat_token = chat_token
        self.chat_agent = chat_agent
        self.compare_branch = compare_branch
        self.output_dir = output_dir
        self.system_content = system_content
        self.prompt_content = prompt_content
        self.data_preparer = data_preparer
        self.reviewer = reviewer
        self.pipeline = pipeline
        self.result_file = result_file
        self.chat_model = chat_model
        self.exclude_file_exc: list[str] | None = (None,)

    @classmethod
    def create(
        cls,
        chat_token: str,
        chat_agent: str,
        compare_branch: str,
        system_content: str,
        prompt_content: str,
        result_file: str,
        output_dir: str,
        chat_model: str | None = None,
        exclude_file_ext: list[str] | None = None,
    ) -> 'CodeSpector':
        agent_info = AgentInfo.create(
            chat_agent=chat_agent,
            chat_token=chat_token,
            chat_model=chat_model,
        )
        data_preparer = CodeSpectorDataPreparer(
            output_dir=output_dir,
            compare_branch=compare_branch,
            exclude_file_ext=exclude_file_ext,
        )
        reviewer = CodeSpectorReviewer(
            diff_file=data_preparer.combined_file,
            chat_token=chat_token,
            chat_agent=chat_agent,
            system_content=system_content,
            output_dir=output_dir,
            chat_model=chat_model,
            agent_info=agent_info,
            prompt_content=prompt_content,
            result_file=result_file,
        )
        pipeline = [data_preparer, reviewer]

        return CodeSpector(
            chat_token=chat_token,
            chat_agent=chat_agent,
            chat_model=chat_model,
            compare_branch=compare_branch,
            system_content=system_content,
            prompt_content=prompt_content,
            data_preparer=data_preparer,
            reviewer=reviewer,
            pipeline=pipeline,
            output_dir=output_dir,
            result_file=result_file,
            exclude_file_ext=exclude_file_ext,
        )

    def review(self):
        for pipe in self.pipeline:
            pipe.start()
