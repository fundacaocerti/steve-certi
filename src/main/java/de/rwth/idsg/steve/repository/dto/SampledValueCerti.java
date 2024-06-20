/*
 * SteVe - SteckdosenVerwaltung - https://github.com/steve-community/steve
 * Copyright (C) 2013-2024 SteVe Community Team
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

import jooq.steve.db.tables.records.TransactionStartRecord;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.jetbrains.annotations.Nullable;
import org.joda.time.DateTime;

import de.rwth.idsg.steve.repository.dto.TransactionDetails;
import java.util.List;

@Getter
public class SampledValueCerti {
    private final String value, context, format, measurand, location, unit;

    // New in OCPP 1.6
    private final String phase;

    public SampledValueCerti(TransactionDetails.MeterValues meterValuesSteve)
    {
        value = meterValuesSteve.getValue();
        context = meterValuesSteve.getReadingContext();
        format = meterValuesSteve.getFormat();
        measurand = meterValuesSteve.getMeasurand();
        location = meterValuesSteve.getLocation();
        unit = meterValuesSteve.getUnit();
        phase = meterValuesSteve.getPhase();

    }
    
}