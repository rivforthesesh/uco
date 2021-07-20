import sims4.commands
import sims4.log  # needed??
import sims4.telemetry
from functools import wraps

__enable_native_commands = True
try:
    import _commands
except:
    __enable_native_commands = False

logger = sims4.commands.logger
NO_CONTEXT = sims4.commands.NO_CONTEXT
lim = 1023  # limit on number of characters that the output allows


def cheat_output(s, context):
    if __enable_native_commands:
        if context != NO_CONTEXT:
            if len(s) < lim:
                # output is under the limit
                _commands.output(s, context)
            else:
                # get maximum length of a word
                max_len = max([len(w) for w in s.split(' ')])

                # split on space for readability if possible
                if max_len > lim:
                    # maximum length is over the limit => just split on first lim characters
                    split_at = lim
                else:
                    # find position of the last space before the limit
                    split_at = s.rfind(' ', 0, lim)

                # split string at that position and output the left part
                _commands.output(s[:split_at], context)
                # call command again on the right part
                cheat_output(s[(split_at+1):], context)
        else:
            logger.always(s)


# replace original
sims4.commands.cheat_output = cheat_output


# testing function
@sims4.commands.Command('riv_uco_test', command_type=sims4.commands.CommandType.Live)
def console_set_m(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    good_msg = 'but if you see this, uco is fine!'
    bad_msg = 'if there\'s nothing below this, uco broke '
    output(' '*(lim-len(bad_msg)-1) + bad_msg + good_msg)
