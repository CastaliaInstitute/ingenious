Identify and split large files across the codebase:

1. **Identify candidates** (any of these criteria):
   - Files >500 lines
   - Files with >5 distinct classes/functions handling different concerns
   - Files with multiple unrelated responsibilities
   - Files that violate Single Responsibility Principle

2. **Split strategy**:
   - **Backend**: Separate by domain/functionality (models, services, utils, validators)
   - **Frontend**: Split by feature/component (blueprints, services, templates)
   - **Shared code**: Extract common utilities to separate modules

3. **File organization**:
   - Create logical module structure (e.g., `services/chat_services/` → split by conversation type)
   - Update imports across codebase
   - Maintain backward compatibility with existing imports
   - Add `__init__.py` files for clean public APIs

4. **Quality checks**:
   - Ensure tests still pass after refactoring
   - Verify no circular import issues
   - Check that each new file has clear, single purpose
   - Update documentation/comments as needed

Prioritize files causing the most maintenance friction or merge conflicts.
