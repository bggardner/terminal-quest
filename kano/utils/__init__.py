# audio.py
import os
def play_sound(audio_file, background=False, delay=0):
    from kano.logging import logger

    # Check if file exists
    if not os.path.isfile(audio_file):
        logger.error('audio file not found: {}'.format(audio_file))
        return False

    _, extension = os.path.splitext(audio_file)

    if extension in ['.wav', '.voc', '.raw', '.au']:
        cmd = 'aplay -q {}'.format(audio_file)
    else:
        volume_percent = get_volume()
        volume_str = '--vol {}'.format(
            percent_to_millibel(volume_percent, raspberry_mod=True))

        # Set the audio output between HDMI or Jack. Default is HDMI since it's the
        # safest route given the PiHat lib getting destabilised if Jack is used.
        audio_out = 'hdmi'
        try:
            from kano_settings.system.audio import is_HDMI
            if not is_HDMI():
                audio_out = 'local'
        except Exception:
            pass

        cmd = 'omxplayer -o {audio_out} {volume} {link}'.format(
            audio_out=audio_out,
            volume=volume_str,
            link=audio_file
        )

    logger.debug('cmd: {}'.format(cmd))

    # Delay the sound playback if specified
    if delay:
        cmd = '/bin/sleep {} ; {}'.format(delay, cmd)

    if background:
        run_bg(cmd)
        rc = 0
    else:
        dummy, dummy, rc = run_cmd_log(cmd)

    return rc == 0


def percent_to_millibel(percent, raspberry_mod=False):
    if not raspberry_mod:
        from math import log10

        multiplier = 2.5

        percent *= multiplier
        percent = min(percent, 100. * multiplier)
        percent = max(percent, 0.000001)

        millibel = 1000 * log10(percent / 100.)

    else:
        # special case for mute
        if percent == 0:
            return -11000

        min_allowed = -4000
        max_allowed = 400
        percent = percent / 100.
        millibel = min_allowed + (max_allowed - min_allowed) * percent

    return int(millibel)


def get_volume():
    from kano.logging import logger

    percent = 100

    cmd = "amixer | head -n 6 | grep -Po '(\d{1,3})(?=%)'"  # noqa
    output, _, _ = run_cmd(cmd)

    try:
        percent = int(output.strip())
    except Exception:
        msg = 'amixer format bad for percent, output: {}'.format(output)
        logger.error(msg)
        pass

    return percent


def set_volume(percent):
    cmd = 'amixer set Master {}%'.format(percent)
    run_cmd(cmd)

# file_operations.py
import json
import os

def read_file_contents(path):
    if os.path.exists(path):
        with open(path) as infile:
            return infile.read().strip()

def read_file_contents_as_lines(path):
    if os.path.exists(path):
        with open(path) as infile:
            content = infile.readlines()
            lines = [line.strip() for line in content]
            return lines

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makdirs(directory)

def chown_path(path, usr=None, group=None):
    user_unsudoed = get_user_unsudoed()
    if not user:
        user = user_unsudoed
    if not group:
        group = user_unsudoed
    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = grp.getgrnam(group).gr_gid
        os.chown(path, uid, gid)
    except KeyError as e:
        from kano.logging import logger
        logger.error(
            'user {} or group {} do not match with existing'.format(user, group))
        ret_val = False
    except OSError as e:
        from kano.logging import logger
        logger.error(
            'Error while trying to chown, root priviledges needed {}'.format(e))
        ret_val = False
    else:
        ret_val = True
    return ret_val


def read_json(filepath, silent=True):
    try:
        return json.loads(read_file_contents(filepath))
    except Exception:
        if not silent:
            raise

def write_json(filepath, data, prettyprint=False, sort_keys=True):
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=2, sort_keys=sort_keys)
    if prettyprint:
        _, _, rc = run_cmd('which underscore')
        if rc == 0:
            cmd = 'underscore print -i {filepath} -o {filepath}'.format(filepath=filepath)
            run_cmd(cmd)

# hardware.py
RPI_A_KEY = 'RPI/A'
RPI_A_PLUS_KEY = 'RPI/A+'
RPI_B_BETA_KEY = 'RPI/B (Beta)'
RPI_B_KEY = 'RPI/B'
RPI_B_PLUS_KEY = 'RPI/B+'
RPI_ZERO_KEY = 'RPI/Zero'
RPI_ZERO_W_KEY = 'RPI/Zero/W'
RPI_COMPUTE_KEY = 'RPI/Compute'
RPI_COMPUTE_3_KEY = 'RPI/Compute/3'
RPI_2_B_KEY = 'RPI/2/B'
RPI_3_KEY = 'RPI/3'
RPI_3_PLUS_KEY = 'RPI/3/B+'


# "performance" scores for RPi boards
RPI_A_SCORE = 1000
RPI_A_PLUS_SCORE = 1000
RPI_B_SCORE = 2000
RPI_B_PLUS_SCORE = 2000
RPI_ZERO_SCORE = 3000
RPI_ZERO_W_SCORE = 3000
RPI_COMPUTE_SCORE = 4000
RPI_2_B_SCORE = 5000
RPI_COMPUTE_3_SCORE = 7000
RPI_3_SCORE = 7000
RPI_3_PLUS_SCORE = 8000

RPI_1_CPU_PROFILE = 'rpi_1'
RPI_2_CPU_PROFILE = 'rpi_2'
RPI_3_CPU_PROFILE = 'rpi_3'

CPUINFO_FILE = '/proc/cpuinfo'


'''
Lookup table with keys as given by get_rpi_model() containing:
    * Human readable 'name' of the board
    * 'cpu_profile' which details the settings to use
    * 'performance' scores
'''
BOARD_PROPERTIES = {
    RPI_A_KEY: {
        'name': 'Raspberry Pi A',
        'cpu_profile': RPI_1_CPU_PROFILE,
        'performance': RPI_A_SCORE,
        'arch': "armv6"
    },
    RPI_A_PLUS_KEY: {
        'name': 'Raspberry Pi A+',
        'cpu_profile': RPI_1_CPU_PROFILE,
        'performance': RPI_A_PLUS_SCORE,
        'arch': "armv6"
    },
    RPI_B_BETA_KEY: {
        'name': 'Raspberry Pi B (Beta)',
        'cpu_profile': RPI_1_CPU_PROFILE,
        'performance': RPI_B_SCORE,
        'arch': "armv6"
    },
    RPI_B_KEY: {
        'name': 'Raspberry Pi B',
        'cpu_profile': RPI_1_CPU_PROFILE,
        'performance': RPI_B_SCORE,
        'arch': "armv6"

    },
    RPI_B_PLUS_KEY: {
        'name': 'Raspberry Pi B+',
        'cpu_profile': RPI_1_CPU_PROFILE,
        'performance': RPI_B_PLUS_SCORE,
        'arch': "armv6"

    },
    RPI_ZERO_KEY: {
        'name': 'Raspberry Pi Zero',
        'cpu_profile': RPI_1_CPU_PROFILE,
        'performance': RPI_ZERO_SCORE,
        'arch': "armv6"

    },
    RPI_ZERO_W_KEY: {
        'name': 'Raspberry Pi Zero Wireless',
        'cpu_profile': RPI_1_CPU_PROFILE,
        'performance': RPI_ZERO_SCORE,
        'arch': "armv6"
    },
    RPI_COMPUTE_KEY: {
        'name': 'Raspberry Pi Compute Module',
        'cpu_profile': RPI_1_CPU_PROFILE,
        'performance': RPI_COMPUTE_SCORE,
        'arch': "armv6"
    },
    RPI_COMPUTE_3_KEY: {
        'name': 'Raspberry Pi Compute Module 3',
        'cpu_profile': RPI_3_CPU_PROFILE,
        'performance': RPI_3_SCORE,
        'arch': "armv8"
    },
    RPI_2_B_KEY: {
        'name': 'Raspberry Pi 2',
        'cpu_profile': RPI_2_CPU_PROFILE,
        'performance': RPI_2_B_SCORE,
        'arch': "armv7"
    },
    RPI_3_KEY: {
        'name': 'Raspberry Pi 3',
        'cpu_profile': RPI_3_CPU_PROFILE,
        'performance': RPI_3_SCORE,
        'arch': 'armv8'
    },
    RPI_3_PLUS_KEY: {
        'name': 'Raspberry Pi 3 B+',
        'cpu_profile': RPI_3_CPU_PROFILE,
        'performance': RPI_3_PLUS_SCORE,
        'arch': 'armv8'
    }
}


_g_revision = None


def get_board_property(board_key, prop):
    board = BOARD_PROPERTIES.get(board_key)

    if not board:
        return

    board_prop = board.get(prop)

    if not board_prop:
        return

    return board_prop

def get_rpi_model(revision=None, use_cached=True):
    """Get the model key of the Rasperry Pi.
    Source for Raspberry Pi model numbers documented at:
    https://www.raspberrypi.org/documentation/hardware/raspberrypi/revision-codes/README.md
    http://elinux.org/RPi_HardwareHistory
    Args:
        revision (str): Revision tag as extracted from /proc/cpuinfo.
        use_cached (bool): See :func:`.get_board_revision`.
    Returns:
        str: Model key identifying the Raspberry Pi model (RPI A/A+/B/B+/Zero/
        CM/2B/3), e.g. RPI_3_KEY
    """
    global _g_revision

    try:
        model_name = overclocked = ''

        revision = revision or get_board_revision(use_cached=use_cached)
        try:
            revision_hex = int(revision, 16)
        except ValueError:  # revision might be 'Beta'
            revision_hex = 0

        # The order of checks here is done Descending by Most Likely Model.
        if revision_hex & 0x00FFFFFF in (0x00A02082, 0x00A22082, 0x00A32082, 0x00A52082):
            model_name = RPI_3_KEY

        elif revision_hex & 0x00FFFFFF in (0x00A01040, 0x00A01041, 0x00A21041, 0x00A22042):
            model_name = RPI_2_B_KEY

        elif revision_hex & 0x00FFFFFF == 0x00A020D3:
            model_name = RPI_3_PLUS_KEY

        elif revision_hex & 0x00ff in (0x10, 0x13) or \
                revision_hex & 0x00FFFFFF == 0x00900032:
            model_name = RPI_B_PLUS_KEY

        elif revision_hex & 0x00ff in (0x2, 0x3, 0x4, 0x5, 0x6, 0xd, 0xe, 0xf):
            model_name = RPI_B_KEY

        elif revision_hex & 0x00ff in (0x12, 0x15) or \
                revision_hex & 0x00FFFFFF == 0x00900021:
            model_name = RPI_A_PLUS_KEY

        elif revision_hex & 0x00ff in (0x7, 0x8, 0x9):
            model_name = RPI_A_KEY

        elif revision_hex & 0x00FFFFFF == 0x009000C1:
            model_name = RPI_ZERO_W_KEY

        elif revision_hex & 0x00FFFFFF in (0x00900092, 0x00920092, 0x00900093, 0x00920093):
            model_name = RPI_ZERO_KEY

        elif revision_hex & 0x00FFFFFF == 0x00A020A0:
            model_name = RPI_COMPUTE_3_KEY

        elif revision_hex & 0x00ff in (0x11, 0x14):
            model_name = RPI_COMPUTE_KEY

        elif revision == 'Beta':
            model_name = RPI_B_BETA_KEY

        else:
            model_name = 'unknown revision: {}'.format(revision)
            logger.error('Unknown Raspberry Pi board revision: {}'.format(revision))

        return '{} {}'.format(model_name, overclocked).strip()

    except Exception:
        from kano.logging import logger
        import traceback
        logger.error('Unexpected error: \n{}'.format(traceback.format_exc()))
        return 'Error getting model name'

def get_board_revision(use_cached=True):
    """Get the Raspberry Pi board revision.
    Args:
        use_cached (bool): Read the revision from a cached value or read
            it from the ``/proc/cpuinfo`` file directly.
    Returns:
        str: Hexadecimal value for the Raspberry Pi board revision; emptry
        string if the value could not be read.
    """
    global _g_revision

    if use_cached and _g_revision:
        return _g_revision

    for entry in reversed(read_file_contents_as_lines(CPUINFO_FILE)):
        if entry.startswith('Revision'):
            _g_revision = entry.split(':')[1].strip()
            return _g_revision

    return ''

def has_min_performance(score):
    """
    Check if the hardware we're running on has a minimum given performance.
    This can be used to abstract the hardware and judge whether a certain
    feature can be enabled due to its performance requriements.
    Args:
        score (int): A performance score just like the ones in PERFORMANCE_SCORES
    Returns:
        bool: True if the hardware has a higher score than the given or if the
              hardware could not be detected; and False otherwise
    """

    model = get_rpi_model()
    model_score = get_board_property(model, 'performance')

    return not model_score or model_score >= score

# misc.py
import datetime

def get_date_now():
    return datetime.datetime.utcnow().isoformat()

# shell.py
import os
import subprocess

def run_cmd(cmd, localised=False, unsudo=False):
    '''
    Executes cmd, returning stdout, stderr, return code
    if localised is False, LC_ALL will be set to "C"
    '''
    env = os.environ.copy()
    if not localised:
        env['LC_ALL'] = 'C'

    if unsudo and \
            'SUDO_USER' in os.environ and \
            os.environ['SUDO_USER'] != 'root':
        cmd = "sudo -u {} bash -c '{}' ".format(os.environ['SUDO_USER'], cmd)

    process = subprocess.Popen(cmd, shell=True, env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               preexec_fn=restore_signals)

    stdout, stderr = process.communicate()
    returncode = process.returncode
    return stdout, stderr, returncode

def run_cmd_log(cmd, localised=False, unsudo=False):
    '''
    Wrapper against run_cmd but Kano Logging executuion and return code
    '''

    from kano.logging import logger

    out, err, rv = run_cmd(cmd, localised, unsudo)
    logger.info("Command: {}".format(cmd))

    if len(out.strip()) > 0:
        logger.info(out)

    if len(err.strip()) > 0:
        logger.error(err)

    logger.info("Return value: {}".format(rv))

    return out, err, rv

def run_bg(cmd, localised=False, unsudo=False):
    '''
    Starts cmd program in the background
    '''
    env = os.environ.copy()
    if not localised:
        env['LC_ALL'] = 'C'

    if unsudo and \
            'SUDO_USER' in os.environ and \
            os.environ['SUDO_USER'] != 'root':
        cmd = "sudo -u {} bash -c '{}' ".format(os.environ['SUDO_USER'], cmd)

    s = subprocess.Popen(cmd, shell=True, env=env)
    return s

def run_print_output_error(cmd, localised=False):
    o, e, rc = run_cmd(cmd, localised)
    if o or e:
        print('\ncommand: {}'.format(cmd))
    if o:
        print('output:\n{}'.format(o.strip()))
    if e:
        print('\nerror:\n{}'.format(e.strip()))
    return o, e, rc

# user.py
import os
import pwd

def get_user_unsudoed():
    if 'SUDO_USER' in os.environ:
        return os.environ['SUDO_USER']
    elif 'LOGNAME' in os.environ:
        return os.environ['LOGNAME']
    else:
        return 'root'

def get_home_by_username(username):
    return pwd.getpwnam(username).pw_dir
