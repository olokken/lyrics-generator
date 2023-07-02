import { Slider } from "@mui/material";
import React from "react";

interface Props {
    maxLength: number;
    setMaxLength: React.Dispatch<React.SetStateAction<number>>;
}

const CustomSlider = ({ maxLength, setMaxLength }: Props) => {

    const handleChange = (
        event: Event,
        newValue: number | number[]
    ) => {
        setMaxLength(newValue as number);
    };

    return (
        <div>

            <Slider
                value={maxLength}
                onChange={handleChange}
                min={100}
                max={450}
                valueLabelDisplay="auto"
                valueLabelFormat={'Number of words to include: ' + maxLength}
                sx={{ width: 300, backgroundColor: "white", marginBottom: "20px", marginTop: "20px" }}
            />
        </div >
    );
};

export default CustomSlider;
