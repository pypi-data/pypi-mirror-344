# Prune's Captcha

## What is it for?

Captcha helps prevent robots from spamming using your forms.

## Prerequisites

-   To be installed on a Prune Django project that uses poetry or UV

## UV project

### Installation

Run the following command in the console:

```bash
uv add captcha_prune
```

### Updating the captcha

Don't hesitate to regularly run `uv sync --upgrade`, as the captcha evolves with time and our practices!

## Poetry project

### Installation

Run the following command:

```bash
poetry add prune_captcha
```

### Updating the captcha

Don't hesitate to regularly run `poetry update`, as the captcha evolves with time and our practices!

## Captcha Integration

Once the project is launched, the application's URLs need to be linked to the form.

-   When making a **GET** request to the form page, the API must be called via the **creation endpoint**. The response will contain the necessary information to display the captcha.
-   When submitting the form via **POST**, the API must be called via the **verification endpoint**. The response will indicate whether the captcha is valid or not.

## Captcha Display

To display the captcha correctly, use the data received in the response from the creation request. This data includes:

-   the captcha's width and height,
-   the piece's width and height,
-   the current position of the piece,
-   the target position (where the piece should be placed),
-   the expected precision (captcha difficulty level).

# Available Versions

| Version | Date       | Notes                                  |
| ------- | ---------- | -------------------------------------- |
| 1.0.0   | 2025-03-14 | First version of the `captcha` package |
