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

package de.rwth.idsg.steve.repository.impl;

import de.rwth.idsg.steve.repository.dto.BootNotification.Overview;
import de.rwth.idsg.steve.repository.BootNotificationRepository;
import de.rwth.idsg.steve.web.dto.BootNotificationQueryForm;
import jooq.steve.db.tables.ChargeBox;
import lombok.extern.slf4j.Slf4j;
import org.jooq.JoinType;
import org.jooq.DSLContext;
import org.jooq.Record9;
import org.jooq.RecordMapper;
import org.jooq.SelectQuery;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import java.util.List;

import static jooq.steve.db.tables.ChargeBox.CHARGE_BOX;

@Slf4j
@Repository
public class BootNotificationRepositoryImpl implements BootNotificationRepository {

    private final DSLContext ctx;

    @Autowired
    public BootNotificationRepositoryImpl(DSLContext ctx) {
        this.ctx = ctx;
    }

    @Override
    @SuppressWarnings("unchecked")
    public List<Overview> getOverview(BootNotificationQueryForm form) {
        SelectQuery selectQuery = ctx.selectQuery();

        selectQuery.addFrom(CHARGE_BOX);

        selectQuery.addSelect(
                CHARGE_BOX.CHARGE_POINT_VENDOR,
                CHARGE_BOX.CHARGE_POINT_MODEL,
                CHARGE_BOX.CHARGE_POINT_SERIAL_NUMBER,
                CHARGE_BOX.FW_VERSION,
                CHARGE_BOX.ICCID,
                CHARGE_BOX.IMSI,
                CHARGE_BOX.METER_TYPE,
                CHARGE_BOX.METER_SERIAL_NUMBER,
                CHARGE_BOX.CHARGE_BOX_SERIAL_NUMBER
        );

        if (form.isChargeBoxIdSet()) {
            selectQuery.addConditions(CHARGE_BOX.CHARGE_BOX_ID.eq(form.getChargeBoxId()));
        }

        return selectQuery.fetch().map(new UserMapper());
    }

    private static class UserMapper
            implements RecordMapper<Record9<String, String, String, String, String, String, String, String, String>, Overview> {
        @Override
        public Overview map(Record9<String, String, String, String, String, String, String, String, String> r) {
            return Overview.builder()
                .chargePointVendor(r.value1())
                .chargePointModel(r.value2())
                .chargePointSerialNumber(r.value3())
                .fwVersion(r.value4())
                .iccid(r.value5())
                .imsi(r.value6())
                .meterType(r.value7())
                .meterSerialNumber(r.value8())
                .chargeBoxSerialNumber(r.value9())
                .build();
        }
    }
}
