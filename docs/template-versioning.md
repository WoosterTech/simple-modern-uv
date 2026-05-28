# Managing Template Versions with Git Tags

To ensure Copier recognizes changes to your template and prompts users to update, you should bump the template version by creating a new Git tag. Copier uses Git tags to determine the template version and whether updates are available.

**Recommended:** Use [Commitizen](https://commitizen-tools.github.io/commitizen/) to manage commits and versioning. This ensures consistent commit messages and automates version bumps and tagging.

## How to Bump the Template Version


## How to Bump the Template Version (with Commitizen)

1. **Make and Stage Your Changes**
  - Edit your template files as needed.
  - Stage your changes:
    ```sh
    git add .
    ```

2. **Create a Conventional Commit**
  - Use Commitizen to create a commit message:
    ```sh
    uvx --from commitizen cz c
    # or, if you prefer:
    uv run cz c
    ```
  - Follow the prompts to describe your changes.

3. **Bump the Version and Tag**
  - Use Commitizen to bump the version and create a tag:
    ```sh
    uvx --from commitizen cz bump
    # or
    uv run cz bump
    ```
  - This will update the version, create a changelog, and add a Git tag.

4. **Push Commits and Tags to Remote**
  - Push your changes and tags so others (and Copier) can see them:
    ```sh
    git push
    git push --tags
    ```

git commit -m "feat: add new feature to template"
git tag v1.2.0
git push origin v1.2.0

## Example (with Commitizen)
```sh
git add .
uvx --from commitizen cz c
uvx --from commitizen cz bump
git push
git push --tags
```


## Notes
- Copier will detect the latest tag as the template version.
- If you skip tagging, Copier may not recognize your changes as a new version.
- You can list existing tags with:
  ```sh
  git tag
  ```
- To delete a tag (if you made a mistake):
  ```sh
  git tag -d vX.Y.Z
  git push origin --delete vX.Y.Z
  ```

---
For more details, see the [Copier documentation on versioning](https://copier.readthedocs.io/en/stable/updating/#template-versioning).
