# Description of TrackMyPrompt Application Tests

## Tests for traitement_ia

### `test_video`
- Verifies that processing a video generates an existing file.
- Deletes the generated file after the test.

### `test_image`
- Verifies that processing an image generates an existing file.
- Deletes the generated file after the test.

## Tests for LanguageManager

### `test_check_structure`
- Verifies that the path structure is correct.

### `test_setLanguage`
- Verifies that the `setLanguage` method correctly changes the language.

## Tests for Filtre

### `test_promptFiltre_dumb`
- Verifies that the "dumb" filter works correctly.

### `test_promptFiltre_dumb_ts`
- Verifies that the "dumb_ts" filter works correctly.

### `test_promptFiltre_mistral`
- Verifies that the "mistral" filter works correctly with a valid API key.

## Tests for EncyclopediaModel

### `test_model_initial_state`
- Verifies that the initial state of the model is empty.

### `test_load_data_success`
- Verifies that data is loaded correctly from a valid database.

### `test_load_data_database_error`
- Simulates a database error with an invalid database path.

### `test_model_update_data`
- Verifies the update of data in the model.

## Tests for ColorManager

### `test_switchTheme`
- Verifies the switching between "light" and "dark" themes.

## Tests for Backend

### `test_initial_shared_variable`
- Verifies the initial values of shared variables.

### `test_receive_prompt_empty`
- Verifies the behavior when the prompt is empty.

### `test_receive_prompt_with_valid_data`
- Verifies the behavior when the prompt is valid.

### `test_receive_file_with_invalid_url`
- Verifies the behavior when the file URL is invalid.

### `test_receive_file_with_valid_url`
- Verifies the behavior when the file URL is valid.

### `test_toggle_menu`
- Verifies the toggling of the menu.

### `test_untoggle_menu`
- Verifies the toggling of the menu (repeated test).

### `test_signals_emitted`
- Verifies if signals are emitted when toggling the menu.

### `test_get_file_path`
- Verifies the conversion of URLs to local paths.

### `test_handle_media_image`
- Verifies the processing of an image.
