"""Interactive colored terminal demo (rich)."""
import sys

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
except ImportError:
    print("Install rich: pip install rich")
    sys.exit(1)

from human_services.mcp.eligibility_server import check_eligibility
from human_services.agents.orchestrator import HumanServicesOrchestrator
from human_services.compliance.compliance_checker import ComplianceChecker


def scene1_contextually_insane():
    """Scene 1: Agent proposes approval for status 'Active' -> BLOCKED."""
    console = Console()
    console.print(Panel.fit(
        "[bold]Scene 1: The Contextually Insane Agent[/bold]\n"
        "Agent proposes approval for status 'Active'",
        border_style="red",
    ))
    r = check_eligibility(
        "victim_001", "SNAP", 30000, 4, status="Active", enrollment_complete=True
    )
    console.print(f"\n[red]BLOCKED: {r['blocked']}[/red]")
    console.print(f"Eligible: {r['eligible']}")
    console.print(Panel(r["explanation"]["citizen"], title="Citizen Explanation", border_style="yellow"))
    console.print()


def scene2_corrected_action():
    """Scene 2: Same case, status 'Enrolled' -> ALLOWED."""
    console = Console()
    console.print(Panel.fit(
        "[bold]Scene 2: The Corrected Action[/bold]\n"
        "Same case with status 'Enrolled'",
        border_style="green",
    ))
    r = check_eligibility(
        "victim_001", "SNAP", 30000, 4, status="Enrolled", enrollment_complete=True
    )
    console.print(f"\n[green]ALLOWED: {not r['blocked']}[/green]")
    console.print(f"Eligible: {r['eligible']}")
    console.print(Panel(r["explanation"]["citizen"], title="Citizen Explanation", border_style="green"))
    console.print()


def scene3_single_mother():
    """Scene 3: No Wrong Door - Single Mother Job Loss."""
    console = Console()
    console.print(Panel.fit(
        "[bold]Scene 3: No Wrong Door — Single Mother Job Loss[/bold]\n"
        "4 programs evaluated",
        border_style="blue",
    ))
    orch = HumanServicesOrchestrator()
    result = orch.single_mother_scenario()
    table = Table(title="Program Results")
    table.add_column("Program", style="cyan")
    table.add_column("Eligible", style="green")
    table.add_column("Blocked", style="red")
    for r in result["program_results"]:
        table.add_row(
            r["program"],
            str(r["eligible"]),
            str(r.get("blocked", False)),
        )
    console.print(table)
    console.print(f"\nRequires human review: {result['requires_human_review']}")
    console.print()


def scene4_compliance_audit():
    """Scene 4: EU AI Act Compliance Audit."""
    console = Console()
    console.print(Panel.fit(
        "[bold]Scene 4: EU AI Act Compliance Audit[/bold]",
        border_style="magenta",
    ))
    checker = ComplianceChecker()
    report = checker.check_all()
    table = Table(title="Compliance Status")
    table.add_column("Article", style="cyan")
    table.add_column("Status", style="green")
    for req in report.requirements:
        status_style = "green" if req.status == "COMPLIANT" else "red"
        table.add_row(req.requirement_id, f"[{status_style}]{req.status}[/{status_style}]")
    console.print(table)
    console.print(f"\nOverall: {report.overall_status} ({report.compliance_percentage:.0f}%)")
    console.print()


def main():
    console = Console()
    console.print("[bold]Human Services AI Architecture — Demo[/bold]\n")
    scene1_contextually_insane()
    scene2_corrected_action()
    scene3_single_mother()
    scene4_compliance_audit()
    console.print("[green]Demo complete.[/green]")


if __name__ == "__main__":
    main()
