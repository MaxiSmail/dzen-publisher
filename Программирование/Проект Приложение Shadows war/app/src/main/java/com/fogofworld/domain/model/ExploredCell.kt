package com.fogofworld.domain.model

data class ExploredCell(
    val cellId: CellId,
    val exploredAt: Long = System.currentTimeMillis()
)