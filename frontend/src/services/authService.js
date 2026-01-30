/**
 * Authentication service with TanStack Query hooks
 */
import { useMutation } from '@tanstack/react-query';
import apiClient from './api';

// ============================================================================
// API Functions
// ============================================================================

export const patientLogin = async (credentials) => {
    const response = await apiClient.post('/auth/patient-login', credentials);
    return response.data;
};

export const doctorLogin = async (credentials) => {
    const response = await apiClient.post('/auth/doctor-login', credentials);
    return response.data;
};

export const adminLogin = async (credentials) => {
    const response = await apiClient.post('/auth/admin-login', credentials);
    return response.data;
};

// ============================================================================
// TanStack Query Hooks
// ============================================================================

export const usePatientLogin = () => {
    return useMutation({
        mutationFn: patientLogin,
        onSuccess: (data) => {
            // Store user data in localStorage
            localStorage.setItem('user', JSON.stringify(data));
        },
    });
};

export const useDoctorLogin = () => {
    return useMutation({
        mutationFn: doctorLogin,
        onSuccess: (data) => {
            localStorage.setItem('user', JSON.stringify(data));
        },
    });
};

export const useAdminLogin = () => {
    return useMutation({
        mutationFn: adminLogin,
        onSuccess: (data) => {
            localStorage.setItem('user', JSON.stringify(data));
        },
    });
};

// ============================================================================
// Auth Utilities
// ============================================================================

export const getCurrentUser = () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
};

export const logout = () => {
    localStorage.removeItem('user');
    window.location.href = '/';
};

export const isAuthenticated = () => {
    return !!getCurrentUser();
};

export const hasRole = (role) => {
    const user = getCurrentUser();
    return user && user.role === role;
};
