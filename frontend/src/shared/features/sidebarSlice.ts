import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

const sidebarSlice = createSlice({
  name: "sidebar",
  initialState: false as boolean,
  reducers: {
    openSidebar: (_state, action: PayloadAction<boolean>) => action.payload,
  },
});

export const { openSidebar } = sidebarSlice.actions;
export default sidebarSlice.reducer;
