import datetime


class Score:
    def __init__(self, username: str, crossword_date: datetime.date, time_in_seconds: int):
        self._username = username
        self._crossword_date = crossword_date
        self._time_in_seconds = time_in_seconds

    @property
    def username(self) -> str:
        """Returns the username of the player."""
        return self._username

    @property
    def crossword_date(self) -> datetime.date:
        """Returns the unique date that this crossword corresponds to."""
        return self._crossword_date

    @property
    def time_in_seconds(self) -> int:
        """Returns the time in seconds that the player took to complete the crossword
        or None if the crossword has not been completed yet."""
        return self._time_in_seconds


class ScoreCollection:
    def __init__(self, scores: list[Score]):
        """Initializes a ScoreCollection object from a list of scores."""
        self.scores = scores

    def __iter__(self):
        """Returns an iterator over the scores."""
        return iter(self.scores)

    def __str__(self):
        """Returns a string representation of the scores in a formatted table."""
        max_username_length = self._get_max_username_length()
        max_crossword_date_length = self._get_max_crossword_date_length()
        max_time_length = self._get_max_time_length()

        total_length = max_username_length + max_crossword_date_length + max_time_length + 6

        header = (
            f"{'Username':<{max_username_length}} | "
            + f"{'Crossword Date':<{max_crossword_date_length}} | "
            + "Time in Seconds"
        )

        separator = "-" * total_length

        EM_DASH = "\u2014"
        rows = []
        for score in self.scores:
            if score.time_in_seconds is None:
                rows.append(
                    f"{score.username:<{max_username_length}} | "
                    + f"{str(score.crossword_date):<{max_crossword_date_length}} | "
                    + EM_DASH
                )
                continue

            rows.append(
                f"{score.username:<{max_username_length}} | "
                + f"{str(score.crossword_date):<{max_crossword_date_length}} | "
                + str(score.time_in_seconds)
            )

        return "\n".join([header, separator] + rows)

    def _get_max_username_length(self) -> int:
        """Returns the maximum username length, including the header."""
        HEADER_LENGTH = len("Username")
        max_username_length = max(len(score.username) for score in self.scores)
        max_username_length = max(max_username_length, HEADER_LENGTH)
        return max_username_length

    def _get_max_crossword_date_length(self) -> int:
        """Returns the maximum completion date length, including the header."""
        HEADER_LENGTH = len("Completion Date")
        max_completion_date_length = max(len(str(score.crossword_date)) for score in self.scores)
        max_completion_date_length = max(max_completion_date_length, HEADER_LENGTH)
        return max_completion_date_length

    def _get_max_time_length(self) -> int:
        """Returns the maximum time length, including the header."""
        HEADER_LENGTH = len("Time in Seconds")
        max_time_length = max(len(str(score.time_in_seconds)) for score in self.scores)
        max_time_length = max(max_time_length, HEADER_LENGTH)
        return max_time_length
