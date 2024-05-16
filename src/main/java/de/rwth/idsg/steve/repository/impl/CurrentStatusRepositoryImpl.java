/*******************************************************************************
 * Copyright (c) 2024 - Fundação CERTI
 * All rights reserved.
 ******************************************************************************/
package de.rwth.idsg.steve.repository.impl;
import de.rwth.idsg.steve.repository.dto.CurrentStatus.Overview;
import de.rwth.idsg.steve.repository.CurrentStatusRepository;
import de.rwth.idsg.steve.web.dto.CurrentStatusQueryForm;
import jooq.steve.db.tables.ChargeBox;
import lombok.extern.slf4j.Slf4j;
import org.jooq.JoinType;
import org.jooq.DSLContext;
import org.jooq.Record7;
import org.jooq.RecordMapper;
import org.joda.time.DateTime;
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
        // Add the FROM clause
        selectQuery.addFrom(CONNECTOR_STATUS);
        // Add the necessary joins
        selectQuery.addJoin(CONNECTOR, CONNECTOR_STATUS.CONNECTOR_PK.eq(CONNECTOR.CONNECTOR_PK));
        // Execute the query and fetch results
        selectQuery.addSelect(
                CONNECTOR.CONNECTOR_ID,
                CONNECTOR_STATUS.ERROR_CODE,
                CONNECTOR_STATUS.ERROR_INFO,
                CONNECTOR_STATUS.STATUS,
                CONNECTOR_STATUS.STATUS_TIMESTAMP,
                CONNECTOR_STATUS.VENDOR_ERROR_CODE,
                CONNECTOR_STATUS.VENDOR_ID
        );

        if (form.isChargeBoxIdSet()) {
            // Add the WHERE condition
            selectQuery.addConditions(CONNECTOR.CHARGE_BOX_ID.eq(form.getChargeBoxId()));
        }
            
        return selectQuery.fetch().map(new UserMapper());
    }
    private static class UserMapper
            implements RecordMapper<Record7<Integer, String, String, String, org.joda.time.DateTime, String, String>, Overview> {
        @Override
        public Overview map(Record7<Integer, String, String, String, org.joda.time.DateTime, String, String> r) {
            String dateString = r.value5().toString();
            return Overview.builder()
                .connectorId(r.value1().toString())
                .errorCode(r.value2())
                .info(r.value3())
                .status(r.value4())
                .timestamp(dateString)
                .vendorErrorCode(r.value6())
                .vendorId(r.value7())
                .build();
        }
    }
}