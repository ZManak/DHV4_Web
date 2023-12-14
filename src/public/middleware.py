import logging
import time

logger = logging.getLogger(__name__)
accesslog = logging.getLogger(name="access_log")


def link(uri, label=None, parameters=None):
    if label is None:
        label = uri
    if parameters is None:
        parameters = ""

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = "\033]8;{};{}\033\\{}\033]8;;\033\\"

    return escape_mask.format(parameters, uri, label)


class LogMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        start_ts = time.time()

        path_str = link(request.build_absolute_uri(request.get_full_path()), label=str(request.path)[:80].ljust(80))

        if request.user.is_authenticated:
            user = request.user
            user_str = f"{user.pk}/{user}"
        else:
            user_str = "Unauthenticated"

        middle_ts = time.time()
        response = self.get_response(request)
        end_ts = time.time()

        time_taken = end_ts - start_ts
        if time_taken > 1:
            log_with = accesslog.warning
            time_to_mid = middle_ts - start_ts
            time_to_end = end_ts - middle_ts

            time_taken_str = f"{time_taken:.2f}s ({time_to_mid:.2f}s to middleware end, {time_to_end:.2f}s to request end)"
        elif response.status_code >= 400:
            log_with = accesslog.warning
            time_taken_str = f"{time_taken:.2f}s"
        else:
            log_with = accesslog.debug
            time_taken_str = f"{time_taken:.2f}s"

        if response.status_code in [301, 302]:
            # Redirect in progress
            redir_url = response["Location"]

            if redir_url.startswith("/"):
                redir_url = request.build_absolute_uri(redir_url)

            status_code_str = f"{response.status_code} (-> {link(redir_url, response['Location'])})"
        else:
            status_code_str = str(response.status_code)

        log_with(
            f"{request.META['REMOTE_ADDR']} - " f"{request.method} {path_str} " f"[{user_str}] " f"{time_taken_str} - " f"{status_code_str}"
        )

        # Code to be executed for each request/response after
        # the view is called.

        return response
