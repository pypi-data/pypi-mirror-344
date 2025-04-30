from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field
from sqlmodel import select
from cs_mcp.configs import config
from cs_mcp.db.dependencies import get_asession
from cs_mcp.db.models import Ns, Wj

# from cs_mcp.utils import PipeClient, PipeSendData


FormLiteral = Literal["진료실", "접수실", "바이탈사인일괄입력"]
ChartNumberType = Annotated[str, Field(description="차트번호(8자리 숫자)")]


def run_mcp():
    import asyncio
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("ClickMCP")

    @mcp.tool()
    def open_form_tool(form_name: FormLiteral) -> str:
        """윈폼의 폼을 엽니다."""
        # with PipeClient() as client:
        #     client.send(
        #         data=PipeSendData(
        #             type="open_form",
        #             target=form_name,
        #         )
        #     )
        #     message = client.read_message()
        #     return message
        return "성공"

    @mcp.tool()
    def write_progress_note(text: str):
        """경과기록을 작성합니다. 반드시 진료실이 실행되어야 합니다."""
        return "성공"
        # with PipeClient() as client:
        #     client.send(
        #         data=PipeSendData(
        #             type="write_progress_note",
        #             target="진료실",
        #             data={
        #                 "text": text,
        #             },
        #         )
        #     )
        #     message = client.read_message()
        #     return message

    @mcp.tool()
    def load_chart_tool(
        form_name: FormLiteral,
        chart_number: ChartNumberType,
    ) -> str:
        """특정 폼에서 차트를 로드합니다. 차트번호는 8자리 숫자여야 합니다."""
        return "00000001"
        # with PipeClient() as client:
        #     client.send(
        #         data=PipeSendData(
        #             type="load_chart",
        #             target=form_name,
        #             data={
        #                 "form_name": form_name,
        #                 "chart_number": chart_number,
        #             },
        #         )
        #     )
        #     message = client.read_message()
        #     return message

    @mcp.tool()
    async def search_nursing_record(
        chart_number: ChartNumberType,
        start_date: Annotated[str, Field(description="시작일자(yyyyMMdd)")],
        end_date: Annotated[str, Field(description="종료일자(yyyyMMdd)")],
    ):
        """간호기록을 조회합니다.
           간호기간은 종료일자로부터 최대 1달로 제한합니다.

        args:
            chart_number: 차트번호(8자리 숫자)
            start: 시작일자(yyyyMMdd)
            end: 종료일자(yyyyMMdd)
        returns:
            일자: 기록일자
            간호문제: 간호문제
            간호처치: 간호처치
        """

        async with get_asession() as session:

            # session 에서 wj 객체를 가져온다.
            ns = await session.exec(
                select(Ns).where(
                    (Ns.ns_chart == chart_number)
                    & (Ns.ns_ymd >= start_date)
                    & (Ns.ns_ymd <= end_date)
                )
            )
            nss = ns.all()

        return [
            {"일자": ns.ns_ymd, "간호문제:": ns.ns_neyong1, "간호처치": ns.ns_neyong2}
            for ns in nss
        ]

    @mcp.tool()
    async def get_birth_by_chartnum(
        chart: Annotated[str, Field(description="차트번호임.")],
    ) -> str:
        """생년월일을 가져온다. 차트번호를 불러오기 위해서는 get_chart_by_name 를 호출하시오.
        args:
            chart (str): 차트번호
        """

        print("get_birth_by_chartnum called:", chart)
        async with get_asession() as session:

            # session 에서 wj 객체를 가져온다.
            wj = await session.exec(select(Wj).where(Wj.wj_chart == chart))

            return wj.one().wj_birthday

    @mcp.tool()
    async def get_charts_by_name(name: str):
        """이름 정보로 차트번호를 가져온다.
        args:
            name (str): 이름
        """

        print(f"get_charts_by_name called: {name}")

        async with get_asession() as session:

            # session 에서 wj 객체를 가져온다.
            wj = await session.exec(
                select(Wj.wj_auto, Wj.wj_chart).where(Wj.wj_suname == name)
            )
            wjs = wj.all()

        return list[wjs]

    @mcp.tool()
    async def get_ns_by_chart(
        chart: Annotated[str, Field(description="차트번호")],
        symd: Annotated[str, Field(description="시작일자(YYYYMMDD)")],
        eymd: Annotated[str, Field(description="종료일자(YYYYMMDD)")],
    ):
        """차트번호로 간호기록을 가져온다. 반드시 기간 정보를 포함해야한다."""

        async with get_asession() as session:

            # session 에서 wj 객체를 가져온다.
            ns = await session.exec(
                select(Ns).where(
                    (Ns.ns_chart == chart) & (Ns.ns_ymd >= symd) & (Ns.ns_ymd <= eymd)
                )
            )
            nss = ns.all()

        return [
            {"일자": ns.ns_ymd, "간호문제:": ns.ns_neyong1, "간호처치": ns.ns_neyong2}
            for ns in nss
        ]

    class BatchVitalSignData(BaseModel):
        hulap2: Optional[str] = Field(description="수축기 혈압(hulap2)")
        hulap1: Optional[str] = Field(description="이완기 혈압(hulap1)")
        maekbak: Optional[str] = Field(description="맥박(maekbak)")
        hohup: Optional[str] = Field(description="호흡수(hohup)")
        cheon: Optional[str] = Field(description="체온(cheon)")
        weight: Optional[str] = Field(description="체중(weight)")
        height: Optional[str] = Field(description="신장(height)")
        spo2: Optional[str] = Field(description="산소포화도(spo2)")
        intake: Optional[str] = Field(description="맥박 산소포화도(intake)")
        urine: Optional[str] = Field(description="소변량(urine)")
        blood: Optional[str] = Field(description="혈액량(blood)")
        aspiration: Optional[str] = Field(description="흡인량(aspiration)")
        drainage: Optional[str] = Field(description="배액량(drainage)")
        vomitus: Optional[str] = Field(description="구토량(vomitus)")

    @mcp.tool()
    def write_batch_vital_sign_tool(
        vs_data: dict[ChartNumberType, BatchVitalSignData],
    ):
        """바이탈사인을 일괄 입력합니다."""
        return "성공"
        # with PipeClient() as client:
        #     client.send(
        #         data=PipeSendData(
        #             type="write_batch_vital_sign",
        #             target="바이탈사인일괄입력",
        #             data=vs_data,
        #         )
        #     )
        #     message = client.read_message()
        #     return message

    # ========== ========== ========== ========== ==========
    if config.IS_DEBUG:
        asyncio.run(mcp.run_sse_async())
    else:
        asyncio.run(mcp.run_stdio_async())


if __name__ == "__main__":
    run_mcp()
