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
package de.rwth.idsg.steve.web.dto;
import io.swagger.annotations.ApiModelProperty;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
@Getter
@Setter
@ToString
public class CurrentStatusQueryForm {
    @ApiModelProperty(value = "The identifier of the transaction (i.e. charging station)")
    private String chargeBoxId;
    @ApiModelProperty(hidden = true)
    public boolean isChargeBoxIdSet() {
        return chargeBoxId != null;
    }
    @ToString(callSuper = true)
    public static class ForApi extends CurrentStatusQueryForm {
        public ForApi () {
            super();
        }
    }
}