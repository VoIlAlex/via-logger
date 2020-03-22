import datetime


LOG_FILENAME_TODAY = 0


def generate_log_filename(name_type: int = LOG_FILENAME_TODAY):
    if name_type == LOG_FILENAME_TODAY:
        return datetime.datetime.now().strftime('%Y-%b-%d') + '.log'
    else:
        raise AttributeError(
            "There is no filename type with ID - {}".format(
                LOG_FILENAME_TODAY
            )
        )
