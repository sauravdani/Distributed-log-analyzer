package com.saurav.logcollector.controller;

import com.saurav.logcollector.model.Log;
import com.saurav.logcollector.repository.LogRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping("/api/logs")
public class LogController {

    private final LogRepository repo;

    public LogController(LogRepository repo) {
        this.repo = repo;
    }

    @GetMapping
    public List<Log> getLogs() {
        return repo.findAll();
    }

    @PostMapping
    public Log postLog(@RequestBody Log log) {
        return repo.save(log);
    }

    @DeleteMapping("/{id}")
    public void deleteLog(@PathVariable Long id) {
        repo.deleteById(id);
    }

}
