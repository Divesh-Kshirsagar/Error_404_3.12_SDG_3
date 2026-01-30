/**
 * Patient service with TanStack Query hooks
 */
import { useMutation, useQuery } from '@tanstack/react-query';
import apiClient from './api';

// ============================================================================
// API Functions
// ============================================================================

export const registerPatient = async (patientData) => {
    const response = await apiClient.post('/patients/register', patientData);
    return response.data;
};

export const getPatient = async (phoneNumber) => {
    const response = await apiClient.get(`/patients/${phoneNumber}`);
    return response.data;
};

export const createVisit = async ({ phoneNumber, visitData }) => {
    const response = await apiClient.post(`/patients/${phoneNumber}/visits`, visitData);
    return response.data;
};

export const getPatientVisits = async (phoneNumber) => {
    const response = await apiClient.get(`/patients/${phoneNumber}/visits`);
    return response.data;
};

// ============================================================================
// TanStack Query Hooks
// ============================================================================

export const useRegisterPatient = () => {
    return useMutation({
        mutationFn: registerPatient,
    });
};

export const usePatient = (phoneNumber) => {
    return useQuery({
        queryKey: ['patient', phoneNumber],
        queryFn: () => getPatient(phoneNumber),
        enabled: !!phoneNumber,
    });
};

export const useCreateVisit = () => {
    return useMutation({
        mutationFn: createVisit,
    });
};

export const usePatientVisits = (phoneNumber) => {
    return useQuery({
        queryKey: ['patient-visits', phoneNumber],
        queryFn: () => getPatientVisits(phoneNumber),
        enabled: !!phoneNumber,
    });
};
