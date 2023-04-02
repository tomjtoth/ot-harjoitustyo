
```mermaid
---
title: Machine() and m.drive()
---

sequenceDiagram
    main ->> +m: Machine()
    activate m
    m->>m._tank: FuelTank()
    deactivate m
```