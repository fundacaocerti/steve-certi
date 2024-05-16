/*******************************************************************************
 * Copyright (c) 2024 - Fundação CERTI
 * All rights reserved.
 ******************************************************************************/
package de.rwth.idsg.steve.repository;
import de.rwth.idsg.steve.repository.dto.CurrentStatus;
import de.rwth.idsg.steve.web.dto.CurrentStatusQueryForm;
import java.util.List;
public interface CurrentStatusRepository {
    List<CurrentStatus.Overview> getOverview(CurrentStatusQueryForm form);
}