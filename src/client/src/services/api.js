const API_BASE_URL = "http://localhost:5000";

export async function apiRequest(
  endpoint,
  options = {}
) {
  try {
    const response = await fetch(
      `${API_BASE_URL}${endpoint}`,
      {
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          ...(options.headers || {}),
        },
        ...options,
      }
    );

    // User is not authenticated
    if (response.status === 401) {
      throw new Error(
        "Authentication token is missing. Please log in again."
      );
    }

    // User is authenticated but unauthorized
    if (response.status === 403) {
      throw new Error(
        "You do not have permission to perform this action."
      );
    }

    // Other API errors
    if (!response.ok) {
      throw new Error(
        `API request failed with status ${response.status}`
      );
    }

    // Handle empty responses
    const contentType =
      response.headers.get("content-type");

    if (
      contentType &&
      contentType.includes("application/json")
    ) {
      return await response.json();
    }

    return response;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}
