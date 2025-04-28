class HP:
    codes = [
        '''

        ''',
        '''

        ''',
    ]

    @staticmethod
    def text(index):
        """Fetch a specific code based on the index."""
        try:
            return HP.codes[index - 1]
        except IndexError:
            return f"Invalid code index. Please choose a number between 1 and {len(HP.codes)}."
