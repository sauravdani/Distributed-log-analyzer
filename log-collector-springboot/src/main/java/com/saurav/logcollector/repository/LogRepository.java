package com.saurav.logcollector.repository;

import com.saurav.logcollector.model.Log;
import org.springframework.data.jpa.repository.JpaRepository;

public interface LogRepository extends JpaRepository<Log, Long> {
}
