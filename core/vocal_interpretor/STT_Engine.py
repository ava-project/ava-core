"""
    Speech-To-Text class handling for AVA

    STT: We are using CMUSphinx opensource library
    CMUSphinx:
        - English language model
        - Customize dictionnary
"""

from os import path


class STT_Engine():
    """
    PocketSphinx Speech-To-Text implementation
    """

    MODELDIR = "/usr/local/share/pocketsphinx/model"
    HMM_DIR = MODELDIR + "en-us/en-us"

    def __init__(self):
        # ensure the import
        try:
            import pocketsphinx as psphinx
        except:
            import pocketsphinx as psphinx
        # Checking if hmm directory exists
        if not path.exists(HMM_DIR):
            print("hmm_dir in '%s' does not exist!", HMM_DIR)
            raise EnvironmentError
        # Checking for missing files in hmm directory
        missing_hmm_files = []
        for missing_file in ('feat.params', 'mdef', 'means', 'noisedict',
                      'transition_matrices', 'variances'):
            if not path.exists(path.join(HMM_DIR, missing_file)):
                missing_hmm_files.append(missing_file)
        # Checking the rest separately because we need only one of those two files
        mixweights = path.exists(path.join(HMM_DIR, 'mixture_weights'))
        sendump = path.exists(path.join(HMM_DIR, 'sendump'))
        if not mixweights and not sendump:
            missing_hmm_files.append('mixture_weights or sendump')
        if missing_hmm_files:
            print("[Warning] %s : hmm files are missing in hmm directory.", ', '.join(missing_hmm_files))
        # Decoding instance if everything is OK
        config = psphinx.Decoder.default_config()
        config.set_string('-hmm', path.join(HMM_DIR))
        config.set_string('-lm', path.join(HMM_DIR, '.lm.bin'))
        config.set_string('-dict', path.join('static/custom.dict'))
        config.set_string('-logfn', '/dev/null')
        self.decoder = psphinx.Decoder(config)

    def __del__(self):
        self.decoder.end_utt()

    def interpretor(self):
        self.decoder.start_utt()
