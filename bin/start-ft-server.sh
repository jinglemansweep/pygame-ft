#!/bin/bash

echo "Flaschen Taschen Daemon"
echo

if [ -f "./.env" ]; then
  echo "Sourcing local environment file"
  source "./.env"
fi

declare -r led_brightness="${LED_BRIGHTNESS:-50}"
declare -r led_cols="${LED_COLS:-64}"
declare -r led_rows="${LED_ROWS:-64}"
declare -r led_chain="${LED_CHAIN:-1}"
declare -r led_parallel="${LED_PARALLEL:-1}"
declare -r led_slowdown_gpio="${LED_SLOWDOWN_GPIO:-0}"
declare -r led_show_refresh="${LED_SHOW_REFRESH}"
declare -r led_limit_refresh="${LED_LIMIT_REFRESH}"
declare led_extra_args=""

if [ "${LED_SHOW_REFRESH}" == "true" ]; then
  led_extra_args="${led_extra_args} --led-show-refresh"
fi

if [ "${LED_LIMIT_REFRESH}" != "" ]; then
  led_extra_args="${led_extra_args} --led-limit-refresh=${LED_LIMIT_REFRESH}"
fi

echo
echo "--led-brightness:    ${led_brightness}"
echo "--led-cols:          ${led_cols}"
echo "--led-rows:          ${led_rows}"
echo "--led-chain:         ${led_chain}"
echo "--led-parallel:      ${led_parallel}"
echo "--led-slowdown-gpio: ${led_slowdown_gpio}"
echo "--led-<extra-args>:  ${led_extra_args}"
echo

./lib/flaschen-taschen/server/ft-server \
  --led-brightness=${led_brightness} \
  --led-cols=${led_cols} \
  --led-rows=${led_rows} \
  --led-chain=${led_chain} \
  --led-parallel=${led_parallel} \
  --led-slowdown-gpio=${led_slowdown_gpio} \
  ${led_extra_args}

