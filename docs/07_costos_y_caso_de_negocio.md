# 07 · Costos y caso de negocio

> Cifras de orden de magnitud con base en los supuestos de [`01_supuestos.md`](01_supuestos.md). Se refinan en descubrimiento.

## Costo de nube estimado (producción, mensual)

| Componente | Dimensionamiento | USD/mes |
|---|---|---|
| Databricks – jobs batch (ingesta, features, entrenamiento, scoring A) | Job clusters efímeros, spot para entrenamiento | 4.000 |
| Databricks – streaming B | Cluster pequeño 24/7 | 2.500 |
| Event Hubs | Standard, 4 TU | 1.000 |
| Model Serving (B) | 2-6 réplicas CPU con autoescalado | 2.000 |
| ADLS Gen2 + Delta | ~50 TB con ciclo de vida a capa fría | 500 |
| API Management | Standard | 700 |
| Azure OpenAI (agente) | ~300 usuarios internos | 800 |
| Monitor / Log Analytics | Retención 90 días | 500 |
| Data Factory + SHIR | Cargas diarias | 300 |
| **Total producción** | | **≈ 12.300 USD ≈ COP 49 M/mes** |
| Dev + Stg (≈ 30% de prod, apagado nocturno) | | ≈ 3.700 USD |
| **Total nube** | | **≈ 16.000 USD/mes ≈ COP 770 M/año** |

**Palancas de costo aplicadas**
- Solo B en tiempo real; A en batch (ahorra ~60% frente a todo en streaming).
- Job clusters efímeros + instancias spot en entrenamiento.
- Dev/Stg apagados fuera de horario y con datos muestreados.
- Model Serving con mínimo de réplicas fuera de pico.

## Costo de equipo (MVP de 12 semanas)
| Rol | Dedicación |
|---|---|
| Data Scientist Senior (líder técnico) | 100% |
| Data Scientist | 100% |
| ML Engineer | 100% |
| Data Engineer | 100% |
| Arquitecto cloud | 30% |
| Validador de modelos (2ª línea) | 20% |
| Product Owner de negocio (riesgo / fraude) | 30% |

## Beneficio estimado (anual, conservador)

| Palanca | Cálculo | COP M/año |
|---|---|---|
| **B – Fraude adicional detectado** | Pérdida COP 25.000 M × 20% de mejora en valor detectado | 5.000 |
| **B – Eficiencia de analistas** | 30% menos falsos positivos ≈ 6 analistas reasignados × COP 80 M | 480 |
| **A – Menor pérdida crediticia** | Pérdida COP 240.000 M × 2% de reducción por gestión preventiva | 4.800 |
| **Total** | | **≈ 10.280** |

**Relación beneficio/costo de nube: ~13x.** Aun si el beneficio real fuera la mitad, el proyecto se paga en el primer año.

Beneficios no cuantificados: mejor experiencia (menos clientes buenos bloqueados), provisiones más precisas (NIIF 9), preaprobados más seguros, base reutilizable para nuevos modelos.

## Árbol de métricas de la solución

```
VALOR (COP ahorrados / año)
├── Fraude evitado (COP)          ← recall en valor @ capacidad (B) ← PR-AUC
├── Pérdida crediticia evitada    ← mora 90+ en bandas D-E gestionadas ← Gini, calibración (A)
├── Eficiencia operativa          ← falsos positivos / 1.000 clientes ← precisión (B)
└── Adopción
    ├── % de alertas atendidas en SLA
    ├── # consultas al agente / usuarios activos
    └── % de acciones de cobranza guiadas por score
CONFIABILIDAD
├── Disponibilidad API ≥ 99,9% · latencia p95 < 100 ms
├── PSI < 0,10 en variables top
└── 100% de scores reproducibles (trazabilidad)
```
