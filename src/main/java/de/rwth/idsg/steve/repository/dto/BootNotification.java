/*
 * SteVe - SteckdosenVerwaltung - https://github.com/steve-community/steve
 * Copyright (C) 2024 Fundação CERTI
 * All Rights Reserved.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

package de.rwth.idsg.steve.repository.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

public final class BootNotification {

    @Getter
    @Builder
    @ToString
    public static final class Overview {

        private final String chargePointVendor;

        private final String chargePointModel;

        private final String chargePointSerialNumber;

        private final String fwVersion;

        private final String iccid;

        private final String imsi;

        private final String meterType;

        private final String meterSerialNumber;

        private final String chargeBoxSerialNumber;
    }
}
