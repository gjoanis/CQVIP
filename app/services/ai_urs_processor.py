from app.database.requirement_repository import RequirementRepository
from app.services.ai_urs_analyzer import AIURSAnalyzer


class AIURSProcessor:

    @staticmethod
    def process(requirements):

        print("=== AI PROCESSOR STARTED ===")

        analyzer = AIURSAnalyzer()

        try:

            for req in requirements:

                print(f"Analyzing {req.req_id}")

                ai = analyzer.analyze(
                    {
                        "req_id": req.req_id,
                        "text": req.text,
                    }
                )

                print(ai)

                req.category = ai.get("category")
                req.criticality = ai.get("criticality")
                req.recommended_verification = ai.get("verification")
                req.risk = ai.get("risk")
                req.gmp_reference = ai.get("gmp_reference")
                req.acceptance_criteria = ai.get("acceptance_criteria")
                req.suggested_test = ai.get("suggested_test")
                req.inspection_concern = ai.get("inspection_concern")
                req.protocol_section = ai.get("protocol_section")
                req.test_steps = ai.get("test_steps", [])
                req.objective_evidence = ai.get("objective_evidence", [])

                RequirementRepository.save(req)

                print(f"Saved {req.req_id}")

            print("=== AI PROCESSOR FINISHED ===")

        except Exception as e:

            print("=== AI PROCESSOR FAILED ===")
            print(type(e).__name__)
            print(e)
            raise