/*
 * SteVe - SteckdosenVerwaltung - https://github.com/steve-community/steve
 * Copyright (C) 2024 FundaÃ§Ã£o CERTI
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

import de.rwth.idsg.steve.repository.dto.CurrentStatus.Overview;
import de.rwth.idsg.steve.repository.CurrentStatusRepository;
import de.rwth.idsg.steve.web.dto.CurrentStatusQueryForm;
import jooq.steve.db.tables.ConnectorStatus;
import jooq.steve.db.tables.ChargeBox;
import lombok.extern.slf4j.Slf4j;
import org.joda.time.DateTime;
import org.jooq.JoinType;
import org.jooq.DSLContext;
import org.jooq.Record7;
import org.jooq.RecordMapper;
import org.jooq.SelectQuery;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import java.util.List;

import java.time.format.DateTimeFormatter;
import static jooq.steve.db.tables.ChargeBox.CHARGE_BOX;
import static jooq.steve.db.tables.Connector.CONNECTOR;
import static jooq.steve.db.tables.ConnectorStatus.CONNECTOR_STATUS;

@Slf4j
@Repository
public class CurrentStatusRepositoryImpl implements CurrentStatusRepository {

    private final DSLContext ctx;

    @Autowired
    public CurrentStatusRepositoryImpl(DSLContext ctx) {
        this.ctx = ctx;
    }

    @Override
    @SuppressWarnings("unchecked")
    public List<Overview> getOverview(CurrentStatusQueryForm form) {
        SelectQuery selectQuery = ctx.selectQuery();

        selectQuery.addFrom(CONNECTOR_STATUS);

        selectQuery.addJoin(CONNECTOR, CONNECTOR_STATUS.CONNECTOR_PK.eq(CONNECTOR.CONNECTOR_PK));
        selectQuery.addOrderBy(CONNECTOR_STATUS.STATUS_TIMESTAMP.desc());

        selectQuery.addSelect(
                CONNECTOR.CONNECTOR_ID,
                CONNECTOR_STATUS.ERROR_CODE,
                CONNECTOR_STATUS.ERROR_INFO,
                CONNECTOR_STATUS.STATUS,
                CONNECTOR_STATUS.STATUS_TIMESTAMP,
                CONNECTOR_STATUS.VENDOR_ERROR_CODE,
                CONNECTOR_STATUS.VENDOR_ID
        );
        selectQuery.addDistinctOn​(CONNECTOR.CONNECTOR_ID);


        if (form.isChargeBoxIdSet()) {
            selectQuery.addConditions(CONNECTOR.CHARGE_BOX_ID.eq(form.getChargeBoxId()));
        }
            
        return selectQuery.fetch().map(new UserMapper());
    }

    private static class UserMapper
            implements RecordMapper<Record7<Integer, String, String, String, DateTime, String, String>, Overview> {
        @Override
        public Overview map(Record7<Integer, String, String, String, DateTime, String, String> r) {
            return Overview.builder()
                .connectorId(r.value1())
                .errorCode(r.value2())
                .info(r.value3())
                .status(r.value4())
                .timestamp(r.value5())
                .vendorErrorCode(r.value6())
                .vendorId(r.value7())
                .build();
        }
    }
}
