import json

keymap = {
	"expand_abbreviation": "ctrl+e",
	"match_pair_outward": "ctrl+d",
	"next_edit_point": "ctrl+alt+right",
	"prev_edit_point": "ctrl+alt+left",
	"toggle_comment": {
		"mac": "super+forward_slash",
		"pc": "ctrl+forward_slash",
		"context": [{
			"key": "selector", 
			"operand": "source.css, text.xml, text.html.basic",
			"operator": "equal"
		}]
	},
	"split_join_tag": {"mac": "shift+super+'", "pc": "shift+ctrl+'"},
	"remove_tag": {"mac": "super+'", "pc": "shift+ctrl+;"},
	"evaluate_math_expression": {"mac": "shift+super+y", "pc": "shift+ctrl+y"},
	"increment_number_by_1": "ctrl+up",
	"decrement_number_by_1": "ctrl+down",
	"increment_number_by_01": "alt+up",
	"decrement_number_by_01": "alt+down",
	"increment_number_by_10": {"mac": "alt+super+up", "pc": "shift+alt+up"},
	"decrement_number_by_10": {"mac": "alt+super+down", "pc": "shift+alt+down"},
	"select_next_item": {"mac": "shift+super+.", "pc": "shift+ctrl+."},
	"select_previous_item": {"mac": "shift+super+,", "pc": "shift+ctrl+,"},
	"reflect_css_value": {"mac": "shift+super+r", "pc": "shift+ctrl+r"},
	"rename_tag": {"mac": "super+shift+k", "pc": "shift+ctrl+backward_slash"},
	"encode_decode_data_url": {"mac": "shift+ctrl+d", "pc": "shift+ctrl+period"},
	"update_image_size": {"mac": "shift+ctrl+i", "pc": "ctrl+u"},

	"expand_as_you_type": {
		"keys": ["ctrl+alt+enter"],
		"context": [{
			"key": "setting.is_widget", 
			"operand": False, 
			"operator": "equal"
		}]
	},

	"wrap_as_you_type": {
		"mac": "ctrl+w", 
		"pc": "shift+ctrl+g",
		"context": [{
			"key": "setting.is_widget", 
			"operand": False, 
			"operator": "equal"
		}]
	},

}

# additional "raw" ST2 actions definition
addon = [
	{
		"keys": ["tab"],
		"command": "expand_abbreviation_by_tab",
		"context": [
			{
				"key": "selector",
				"match_all": True,
				"operand": "source.css, source.sass, source.less, source.scss, source.stylus, text.xml, text.html.basic - source.php - keyword.control.php, text.haml, text.html.ruby, text.html.twig, string",
				"operator": "equal"
			}, {
				"key": "selection_empty",
				"match_all": True
			}, {
				"key": "has_next_field",
				"operator": "equal",
				"operand": False,
				"match_all": True
			}, {
				"key": "setting.disable_tab_abbreviations",
				"operator": "equal",
				"operand": False,
				"match_all": True
			}, {
				"key": "auto_complete_visible",
				"operand": False,
				"operator": "equal",
				"match_all": True
			}, {
				"key": "is_abbreviation",
				"match_all": True
			}
		]
	},

	# behaviour of tab key when autocomplete popup is visible
	{
		"keys": ["tab"],
		"command": "expand_abbreviation_by_tab",
		"context": [
			{
				"key": "selector",
				"match_all": True,
				"operand": "source.css, source.sass, source.less, source.scss, source.stylus, text.xml, text.html.basic - source.php - keyword.control.php, text.haml, text.html.ruby, text.html.twig, string",
				"operator": "equal"
			}, {
				"key": "selection_empty",
				"match_all": True
			}, {
				"key": "has_next_field",
				"operator": "equal",
				"operand": False,
				"match_all": True
			}, {
				"key": "auto_complete_visible",
				"operator": "equal",
				"operand": True,
				"match_all": True
			}, {
				"key": "setting.disable_tab_abbreviations_on_auto_complete",
				"operator": "equal",
				"operand": False,
				"match_all": True
			}, {
				"key": "is_abbreviation",
				"match_all": True
			}
		]
	}, 

	# insert linebreak with formatting
	{
		"keys": ["enter"],
		"command": "handle_enter_key",
		"context": [
			{
				"key": "selector",
				"operand": "text.html.basic -source, text.xml, text.html.ruby, text.html.twig"
			}, {
				"key": "auto_complete_visible",
				"operand": False
			}, {
				"key": "setting.disable_formatted_linebreak",
				"operand": False
			}
		]
	},

	{
		"keys": ["#"],
		"command": "emmet_insert_attribute",
		"args": {"attribute": "id"},
		"context": [
			{
				"key": "selector",
				"match_all": True,
				"operand": "text.html meta.tag -string -punctuation.definition.tag.begin.html -meta.scope.between-tag-pair.html -source -meta.tag.template.value.twig",
				"operator": "equal"
			}, {
				"key": "setting.auto_id_class",
				"operator": "equal",
				"operand": True
			}
		]
	},

	{
		"keys": ["."],
		"command": "emmet_insert_attribute",
		"args": {"attribute": "class"},
		"context": [
			{
				"key": "selector",
				"match_all": True,
				"operand": "text.html meta.tag -string -punctuation.definition.tag.begin.html -meta.scope.between-tag-pair.html -source -meta.tag.template.value.twig",
				"operator": "equal"
			}, {
				"key": "setting.auto_id_class",
				"operator": "equal",
				"operand": True
			}
		]
	}
]

standalone_actions = ["wrap_as_you_type", "expand_as_you_type"]

def create_record(k, v, os_type):
	if isinstance(v, basestring):
		v = {"keys": [v]}

	if os_type in v:
		v['keys'] = [v[os_type]]

	if 'pc' in v:
		del v['pc'] 
	
	if 'mac' in v:
		del v['mac']

	if k in standalone_actions:
		v['command'] = k
	else:
		v['command'] = 'run_emmet_action'
		v['args'] = {"action": k}

	if 'context' not in v:
		v['context'] = []

	v['context'].append({'key': 'setting.enable_emmet_keymap'})

	if len(v['context']) > 1:
		for ctx in v['context']:
			ctx['match_all'] = True

	return v

def generate_keymap_file(path):
	os_type = 'mac' if '(OSX)' in path else 'pc'

	editor_keymap = [create_record(k, v, os_type) for k, v in keymap.items()] + addon
	content = json.dumps(editor_keymap, indent=4)
	f = open(path, 'w')
	f.write(content)
	f.close()

for path in ['../Default (OSX).sublime-keymap']:
	print('Generate %s' % path)
	generate_keymap_file(path)


