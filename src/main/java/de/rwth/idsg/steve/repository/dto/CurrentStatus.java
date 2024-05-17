/*******************************************************************************
 * Copyright (c) 2024 - Fundação CERTI
 * All rights reserved.
 ******************************************************************************/
package de.rwth.idsg.steve.repository.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.ToString;
import org.joda.time.DateTime;

public final class CurrentStatus {

    @Getter
    @Builder
    @ToString
    public static final class Overview {
        private final Integer connectorId;

        private final String errorCode;

        private final String info;

        private final String status;

        private final DateTime timestamp;

        private final String vendorErrorCode;

        private final String vendorId;
    }
}
