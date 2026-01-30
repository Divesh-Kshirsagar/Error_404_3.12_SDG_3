/**
 * Doctor service with TanStack Query hooks
 */
import { useMutation, useQuery } from '@tanstack/react-query';
import apiClient from './api';

// ============================================================================
// API Functions
// ============================================================================

export const getDoctorQueue = async (doctorId) => {
    const response = await apiClient.get(`/doctors/${doctorId}/queue`);
    return response.data;
};

export const getVisitDetails = async (visitId) => {
    const response = await apiClient.get(`/doctors/visits/${visitId}`);
    return response.data;
};

export const updateVisit = async ({ visitId, updateData }) => {
    const response = await apiClient.put(`/doctors/visits/${visitId}`, updateData);
    return response.data;
};

export const startVisit = async ({ visitId, doctorId }) => {
    const response = await apiClient.post(`/doctors/visits/${visitId}/start?doctor_id=${doctorId}`);
    return response.data;
};

// ============================================================================
// TanStack Query Hooks
// ============================================================================

export const useDoctorQueue = (doctorId) => {
    return useQuery({
        queryKey: ['doctor-queue', doctorId],
        queryFn: () => getDoctorQueue(doctorId),
        enabled: !!doctorId,
        refetchInterval: 30000, // Refresh every 30 seconds
    });
};

export const useVisitDetails = (visitId) => {
    return useQuery({
        queryKey: ['visit-details', visitId],
        queryFn: () => getVisitDetails(visitId),
        enabled: !!visitId,
    });
};

export const useUpdateVisit = () => {
    return useMutation({
        mutationFn: updateVisit,
    });
};

export const useStartVisit = () => {
    return useMutation({
        mutationFn: startVisit,
    });
};
