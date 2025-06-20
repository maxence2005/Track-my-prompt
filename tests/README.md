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

## Tests for Historique (History)

### `test_EX1_T1_affichage_historique_nominal_1`
- Adds a history entry and checks its presence.

### `test_EX1_T2_ajout_multiples`
- Adds multiple entries and checks their order.

### `test_EX1_T3_modif_pendant_traitement`
- Simulates blocking modification during processing.

### `test_EX1_T4_click_rapide`
- Ensures no duplication on rapid clicks.

### `test_EX1_T5_affichage_limite`
- Adds more than 50 entries and checks the limit.

### `test_EX2_T1_modif_prompt`
- Modifies an existing prompt and checks the update.

### `test_EX2_T3_prompt_vide`
- Ensures empty prompts are rejected.

### `test_EX2_T5_prompt_100_caracteres`
- Checks handling of a 100-character prompt.

### `test_EX3_T1_suppression_nominale`
- Tests simple deletion of an entry.

### `test_EX3_T2_suppression_second_element`
- Tests deletion of a second entry.

### `test_EX3_T3_suppression_en_detection`
- Ensures deletion is blocked during detection.

### `test_EX3_T4_suppression_rapide`
- Ensures no error on rapid double deletion.

### `test_EX3_T5_suppression_massive`
- Tests mass deletion of entries.

---

## Tests for AudioRecorder (Transcription)

### `test_EX5_T1_transcription_nominale`
- Checks correct transcription of a clear message.

### `test_EX5_T2_bruit_uniquement`
- Ensures transcription fails on noise-only input.

### `test_EX5_T3_transcription_mot_complexe`
- Checks transcription of a complex/rare word.

### `test_EX5_T4_aucun_son`
- Ensures error is raised if no sound is recorded.

### `test_EX5_T5_duree_maximale`
- Tests handling of a very long recording.

### `test_EX5_T6_callback_transcription`
- Checks that the callback is called during transcription.

---