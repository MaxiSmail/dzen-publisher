package com.fogofworld.domain.model

data class LatLng(
    val latitude: Double,
    val longitude: Double
) {
    companion object {
        fun fromPair(pair: Pair<Double, Double>): LatLng = LatLng(pair.first, pair.second)
    }
}