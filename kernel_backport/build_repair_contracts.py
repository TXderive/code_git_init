from dataclasses import dataclass, field

from kernel_backport.contracts import (
    FullBuildResult,
    ProjectContext,
)


@dataclass
class BuildAttributionCandidate:
    cve: str = ""
    patch_ref: str = ""
    series_line: str = ""
    series_index: int = 0

    matched_files: list[str] = field(
        default_factory=list
    )

    patch_files: list[str] = field(
        default_factory=list
    )

    match_type: str = "file_overlap"
    confidence: str = "candidate"
    batch_related: bool = False

    reason: str = ""
    patch_excerpt: str = ""


@dataclass
class BuildSourceContext:
    file: str = ""
    line: int = 0
    snippet: str = ""


@dataclass
class BuildHistoryHint:
    file: str = ""
    commit: str = ""
    subject: str = ""

    reason: str = (
        "recent history touching error file"
    )


@dataclass
class BuildRepairEvidence:
    run_id: str = ""
    repair_id: str = ""
    build_id: str = ""

    status: str = "blocked"
    next_action: str = "none"

    failure_kind: str = ""
    failure_stage: str = ""

    build_input_ref: str = ""
    build_errors_ref: str = ""
    diagnostics_ref: str = ""

    kernel_root: str = ""
    hulk_root: str = ""

    applied_cves: list[str] = field(
        default_factory=list
    )

    build_errors: list[dict] = field(
        default_factory=list
    )

    source_contexts: list[
        BuildSourceContext
    ] = field(
        default_factory=list
    )

    candidates: list[
        BuildAttributionCandidate
    ] = field(
        default_factory=list
    )

    history_hints: list[
        BuildHistoryHint
    ] = field(
        default_factory=list
    )

    unattributed_errors: list[dict] = field(
        default_factory=list
    )

    attribution_note: str = (
        "Candidate attribution is correlation "
        "only. A patch touching an error file "
        "is not proof that the patch caused "
        "the build failure."
    )

    evidence_ref: str = ""

    errors: list[str] = field(
        default_factory=list
    )


@dataclass
class BuildRepairProposal:
    proposal_type: str = "manual_review"

    target_cve: str = ""
    target_patch_ref: str = ""

    candidate_commit: str = ""

    reason: str = ""
    confidence: str = "low"

    instructions: list[str] = field(
        default_factory=list
    )

    provider: str = ""
    raw_response: str = ""


@dataclass
class BuildRepairAnalysisRequest:
    run_id: str = ""
    repair_id: str = ""
    build_id: str = ""

    run_dir: str = ""

    config_path: str = "config.json"
    agent_provider: str = "direct_llm"

    build_input_ref: str = ""
    build_errors_ref: str = ""
    diagnostics_ref: str = ""

    mock_proposal_type: str = ""
    mock_target_cve: str = ""
    mock_target_patch_ref: str = ""
    mock_candidate_commit: str = ""
    mock_reason: str = ""


@dataclass
class CollectBuildRepairEvidenceInput:
    context: ProjectContext | None = None

    request: BuildRepairAnalysisRequest = field(
        default_factory=BuildRepairAnalysisRequest
    )


@dataclass
class AnalyzeBuildRepairInput:
    evidence: BuildRepairEvidence = field(
        default_factory=BuildRepairEvidence
    )

    config_path: str = "config.json"
    agent_provider: str = "direct_llm"

    mock_proposal_type: str = ""
    mock_target_cve: str = ""
    mock_target_patch_ref: str = ""
    mock_candidate_commit: str = ""
    mock_reason: str = ""


@dataclass
class BuildRepairAnalysisResult:
    run_id: str = ""
    repair_id: str = ""
    build_id: str = ""

    status: str = "blocked"
    next_action: str = "none"

    evidence: BuildRepairEvidence = field(
        default_factory=BuildRepairEvidence
    )

    proposal: BuildRepairProposal = field(
        default_factory=BuildRepairProposal
    )

    result_ref: str = ""

    errors: list[str] = field(
        default_factory=list
    )


@dataclass
class PersistBuildRepairAnalysisInput:
    run_dir: str = ""
    repair_id: str = ""

    result: BuildRepairAnalysisResult = field(
        default_factory=BuildRepairAnalysisResult
    )


#
# Step 4
#


@dataclass
class BuildRepairMaterialization:
    status: str = "blocked"
    next_action: str = "none"

    diff_text: str = ""
    reason: str = ""

    provider: str = ""
    raw_response: str = ""

    errors: list[str] = field(
        default_factory=list
    )


@dataclass
class MaterializeBuildRepairInput:
    evidence: BuildRepairEvidence = field(
        default_factory=BuildRepairEvidence
    )

    proposal: BuildRepairProposal = field(
        default_factory=BuildRepairProposal
    )

    config_path: str = "config.json"

    mock_diff: str = ""


@dataclass
class BuildRepairTrialResult:
    status: str = "blocked"
    next_action: str = "none"

    proposal_type: str = ""

    target_cve: str = ""
    target_patch_ref: str = ""
    candidate_commit: str = ""

    series_mode: str = ""
    target_series_line: str = ""
    new_series_line: str = ""

    formal_patch_ref: str = ""
    repair_patch_ref: str = ""

    changed_files: list[str] = field(
        default_factory=list
    )

    trial_root: str = ""
    evidence_ref: str = ""

    errors: list[str] = field(
        default_factory=list
    )


@dataclass
class ValidateBuildRepairInput:
    context: ProjectContext | None = None

    run_dir: str = ""
    repair_id: str = ""
    round_id: str = ""

    build_input_ref: str = ""

    evidence: BuildRepairEvidence = field(
        default_factory=BuildRepairEvidence
    )

    proposal: BuildRepairProposal = field(
        default_factory=BuildRepairProposal
    )

    materialization: BuildRepairMaterialization = field(
        default_factory=BuildRepairMaterialization
    )


@dataclass
class BuildRepairCommitResult:
    status: str = "blocked"
    next_action: str = "none"

    repair_patch_ref: str = ""
    series_backup_ref: str = ""
    series_sha256: str = ""

    build_input_ref: str = ""

    created_patch: bool = False
    reused_patch: bool = False

    rollback_performed: bool = False
    rollback_errors: list[str] = field(
        default_factory=list
    )

    evidence_ref: str = ""

    errors: list[str] = field(
        default_factory=list
    )


@dataclass
class CommitBuildRepairInput:
    context: ProjectContext | None = None

    run_id: str = ""
    owner_id: str = ""

    run_dir: str = ""
    repair_id: str = ""
    round_id: str = ""

    build_input_ref: str = ""

    trial: BuildRepairTrialResult = field(
        default_factory=BuildRepairTrialResult
    )


@dataclass
class BuildRepairCycleRequest:
    run_id: str = ""
    repair_id: str = ""

    owner_id: str = ""
    ver: str = ""

    run_dir: str = ""

    expected_head: str = ""

    build_input_ref: str = ""

    applied_cves: list[str] = field(
        default_factory=list
    )

    config_path: str = "config.json"
    agent_provider: str = "direct_llm"

    execution_mode: str = "real"

    max_rounds: int = 3

    initial_build: FullBuildResult = field(
        default_factory=FullBuildResult
    )

    mock_proposal_type: str = ""
    mock_target_cve: str = ""
    mock_target_patch_ref: str = ""
    mock_candidate_commit: str = ""
    mock_reason: str = ""
    mock_repair_diff: str = ""


@dataclass
class BuildRepairCycleResult:
    run_id: str = ""
    repair_id: str = ""

    status: str = "blocked"
    next_action: str = "none"

    rounds: int = 0

    analyses: list[
        BuildRepairAnalysisResult
    ] = field(
        default_factory=list
    )

    commits: list[
        BuildRepairCommitResult
    ] = field(
        default_factory=list
    )

    final_build: FullBuildResult = field(
        default_factory=FullBuildResult
    )

    verified_cves: list[str] = field(
        default_factory=list
    )

    result_ref: str = ""

    errors: list[str] = field(
        default_factory=list
    )


@dataclass
class PersistBuildRepairCycleInput:
    run_dir: str = ""
    repair_id: str = ""

    result: BuildRepairCycleResult = field(
        default_factory=BuildRepairCycleResult
    )
  
