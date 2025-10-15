/*
 * Copyright 2025 Team Aeris
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import { createLogger, format, transports } from "winston";

const customFormat = format.printf(({ level, message, timestamp }) => {
    const date = new Date(timestamp as string);
    const dateStr = date.toLocaleString("ko-KR", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
    }).replace(/\./g, '-').replace(' ', '').replace(/-$/, '');

    let truncatedMessage = String(message)
        .replace(/\n/g, ' ')
        .replace(/\r/g, ' ')
        .replace(/\t/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();

    const maxLength = 100;
    if (truncatedMessage.length > maxLength) {
        truncatedMessage = truncatedMessage.substring(0, maxLength - 3) + '...';
    }

    return `[${dateStr}] [${level}] ${truncatedMessage}`;
});

export const logger = createLogger({
    level: "info",
    format: format.combine(
        format.timestamp(),
        customFormat
    ),
    transports: [new transports.Console()],
});