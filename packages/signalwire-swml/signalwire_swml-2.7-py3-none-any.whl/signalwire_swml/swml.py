import json
from .ordered import get_ordered_dict, dump_yaml

class SignalWireSWML:
    VERSION = '2.0'

    def __init__(self, version='1.0.0'):
        self._content = {
            'version': version,
        }
        self._prompt = {}
        self._params = {}
        self._hints = []
        self._SWAIG = {
            'defaults': {},
            'functions': [],
            'includes': [],
            'native_functions': [],
        }
        self._pronounce = []
        self._languages = []
        self._post_prompt = {}

    def add_aiapplication(self, section):
        app = "ai"
        args = {}
        for data in ['post_prompt', 'post_prompt_url', 'post_prompt_auth_user', 'post_prompt_auth_password',
                     'languages', 'hints', 'params', 'prompt', 'SWAIG', 'pronounce', 'global_data']:
            if hasattr(self, f'_{data}'):
                args[data] = getattr(self, f'_{data}')
        
        self._content.setdefault('sections', {}).setdefault(section, []).append({app: args})

    def set_context_steps(self, context_name, steps):
        self._prompt.setdefault('contexts', {}).setdefault(context_name, {})['steps'] = steps

    def add_context_steps(self, context_name, steps):
        self._prompt.setdefault('contexts', {}).setdefault(context_name, {}).setdefault('steps', []).extend(steps)

    def set_prompt_contexts(self, contexts):
        self._prompt['contexts'] = contexts

    def add_application(self, section, app, args=None):
        if args is None:
            args = {}
        self._content.setdefault('sections', {}).setdefault(section, []).append({app: args})

    def set_aipost_prompt_url(self, postprompt):
        for k, v in postprompt.items():
            setattr(self, f'_{k}', v)

    def set_global_data(self, data):
        self._content['_global_data'] = data

    def set_aiparams(self, params):
        self._params = params

    def add_aiparams(self, params):
        numeric_keys = ['end_of_speech_timeout', 'attention_timeout', 'outbound_attention_timeout',
                        'background_file_loops', 'background_file_volume', 'digit_timeout', 'energy_level']
        
        for k, v in params.items():
            if k in numeric_keys:
                self._params[k] = float(v) if v is not None else 0
            else:
                self._params[k] = v

    def set_aihints(self, hints):
        self._hints = hints

    def add_aihints(self, hints):
        for hint in hints:
            if isinstance(hint, dict):
                hint_str = json.dumps(hint, sort_keys=True)
                exists = False
                for existing_hint in self._hints:
                    if isinstance(existing_hint, dict):
                        existing_str = json.dumps(existing_hint, sort_keys=True)
                        if existing_str == hint_str:
                            exists = True
                            break
                if not exists:
                    self._hints.append(hint)
            elif hint not in self._hints:
                self._hints.append(hint)

    def add_aiswaigdefaults(self, SWAIG):
        for k, v in SWAIG.items():
            self._SWAIG['defaults'][k] = v

    def add_aiswaigfunction(self, SWAIG):
        self._SWAIG['functions'].append(SWAIG)

    def set_aipronounce(self, pronounce):
        self._pronounce = pronounce

    def add_aipronounce(self, pronounce):
        self._pronounce.append(pronounce)

    def set_ailanguage(self, language):
        self._languages = language

    def add_ailanguage(self, language):
        self._languages.append(language)

    def add_aiinclude(self, include):
        if 'url' in include and include['url']:
            self._SWAIG['includes'].append(include)

    def add_ainativefunction(self, native):
        self._SWAIG['native_functions'].append(native)

    def set_aipost_prompt(self, postprompt):
        numeric_keys = ['confidence', 'barge_confidence', 'top_p', 'temperature', 'frequency_penalty', 'presence_penalty']
        for k, v in postprompt.items():
            if k in numeric_keys:
                self._post_prompt[k] = float(v) if v is not None else 0
            else:
                self._post_prompt[k] = v

    def set_aiprompt(self, prompt):
        numeric_keys = ['confidence', 'barge_confidence', 'top_p', 'temperature', 'frequency_penalty', 'presence_penalty']
        for k, v in prompt.items():
            if k in numeric_keys:
                self._prompt[k] = float(v) if v is not None else 0
            else:
                self._prompt[k] = v

    def swaig_response(self, response):
        return response

    def swaig_response_json(self, response):
        return json.dumps(response, indent=4, ensure_ascii=False)

    def clean_empty_items(self):
        keys_to_check = ['functions', 'native_functions', 'includes']
        for key in keys_to_check:
            if key in self._SWAIG and not self._SWAIG[key]:
                del self._SWAIG[key]
                
        self._hints = [hint for hint in self._hints if hint]
        self._pronounce = [pronounce for pronounce in self._pronounce if pronounce]
        self._languages = [language for language in self._languages if language]
        self._params = {k: v for k, v in self._params.items() if v}
        self._post_prompt = {k: v for k, v in self._post_prompt.items() if v}
            
    def render(self, ordered=False):
        """
        Render the SWML configuration as a Python dictionary.
        
        Args:
            ordered (bool, optional): Whether to order the output according to the template. Defaults to False.
        
        Returns:
            dict: The SWML configuration
        """
        self.clean_empty_items()
        if ordered:
            return get_ordered_dict(self._content)
        return self._content

    def render_json(self, ordered=False):
        """
        Render the SWML configuration as a JSON string.
        
        Args:
            ordered (bool, optional): Whether to order the output according to the template. Defaults to False.
        
        Returns:
            str: The JSON string
        """
        self.clean_empty_items()
        content = get_ordered_dict(self._content) if ordered else self._content
        return json.dumps(content, indent=4, ensure_ascii=False)

    def render_yaml(self, ordered=False):
        """
        Render the SWML configuration as a YAML string.
        
        Args:
            ordered (bool, optional): Whether to order the output according to the template. Defaults to False.
        
        Returns:
            str: The YAML string
        """
        self.clean_empty_items()
        content = get_ordered_dict(self._content) if ordered else self._content
        # Always use dump_yaml to avoid !!python/object/apply:collections.OrderedDict
        return dump_yaml(content)

    @staticmethod
    def load_json(path_or_str, from_string=False):
        """
        Load a JSON file (or string if from_string=True) and return the Python object.
        """
        import json
        if from_string:
            return json.loads(path_or_str)
        with open(path_or_str, 'r') as f:
            return json.load(f)

    @staticmethod
    def load_yaml(path_or_str, from_string=False):
        """
        Load a YAML file (or string if from_string=True) and return the Python object.
        """
        import yaml
        if from_string:
            return yaml.safe_load(path_or_str)
        with open(path_or_str, 'r') as f:
            return yaml.safe_load(f)
