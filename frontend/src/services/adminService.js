/**
 * Admin service with TanStack Query hooks
 */
import { useMutation, useQuery } from '@tanstack/react-query';
import apiClient from './api';

// ============================================================================
// API Functions
// ============================================================================

export const getAnalytics = async () => {
    const response = await apiClient.get('/admin/analytics/dashboard');
    return response.data;
};

export const getAllDoctors = async () => {
    const response = await apiClient.get('/admin/doctors');
    return response.data;
};

export const createDoctor = async (doctorData) => {
    const response = await apiClient.post('/admin/doctors', doctorData);
    return response.data;
};

export const deleteDoctor = async (doctorId) => {
    const response = await apiClient.delete(`/admin/doctors/${doctorId}`);
    return response.data;
};

export const getAllVisits = async (status = null) => {
    const url = status ? `/admin/visits?status=${status}` : '/admin/visits';
    const response = await apiClient.get(url);
    return response.data;
};

// ============================================================================
// TanStack Query Hooks
// ============================================================================

export const useAnalytics = () => {
    return useQuery({
        queryKey: ['analytics'],
        queryFn: getAnalytics,
        refetchInterval: 60000, // Refresh every minute
    });
};

export const useAllDoctors = () => {
    return useQuery({
        queryKey: ['all-doctors'],
        queryFn: getAllDoctors,
    });
};

export const useCreateDoctor = () => {
    return useMutation({
        mutationFn: createDoctor,
    });
};

export const useDeleteDoctor = () => {
    return useMutation({
        mutationFn: deleteDoctor,
    });
};

export const useAllVisits = (status = null) => {
    return useQuery({
        queryKey: ['all-visits', status],
        queryFn: () => getAllVisits(status),
    });
};
