/*
 * This file is part of the Head Tracker distribution (https://github.com/dlktdr/headtracker)
 * Copyright (c) 2023 Cliff Blackburn
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

#define INPUT_PULLUP (GPIO_INPUT | GPIO_PULL_UP)
#define NRFPIN(port, pin) ((32 * port) + pin)
#define PIN_TO_NRFPORT(pin) (pin / 32)
#define PIN_TO_NRFPIN(pin) (pin % 32)
#define END_IO_PINS PIN(COUNT, -1, "\0")
#define PIN_NAME_TO_NUM(pin) PinNumber[pin]

extern const char* StrPins[];
