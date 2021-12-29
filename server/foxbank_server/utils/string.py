def str_range_replace(
    input: str,
    replace_with: str,
    range_start: int | None = None,
    range_end: int | None = None,
) -> str:
    return input[:range_start] + replace_with + input[range_end:]
