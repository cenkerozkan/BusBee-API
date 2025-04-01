.PHONY: git_count_lines

git_count_lines:
	echo "Counting lines of code in the git repository"
	@git ls-files '*.py' | xargs wc -l