import { Autocomplete, AutocompleteChangeReason, TextField } from '@mui/material';
import { SyntheticEvent, useEffect } from "react";
import useSWR from 'swr';



interface Props {
    models: string[];
    setModels: React.Dispatch<React.SetStateAction<string[]>>;
    setSelectedModel: React.Dispatch<React.SetStateAction<string>>;
    isLoading: boolean;
}

const CustomAutocomplete = ({ models, setModels, setSelectedModel, isLoading }: Props) => {
    const { data, error } = useSWR('http://localhost:5555/pretrainedModels', url =>
        fetch(url).then(res => res.json())
    );

    useEffect(() => {
        if (data) {
            setModels(data);
        }
    }, [data, setModels])

    const handleAutocompleteChange = (event: SyntheticEvent<Element, Event>, value: string | null, reason: AutocompleteChangeReason) => {
        if (value && (reason === 'selectOption' || reason === 'createOption')) {
            setSelectedModel(value)
        } else if (reason === 'clear') {
            setSelectedModel('');
        } else if (reason === 'createOption') {

        }
    }

    if (!data) {
        return <Autocomplete
            loading={true}
            options={models}
            multiple={false}
            sx={{
                width: 300, backgroundColor: "white",
                marginBottom: "20px"
            }}
            onChange={handleAutocompleteChange}
            renderInput={(params) => <TextField {...params}
                sx={{ "& .MuiInputBase-root": { fontSize: 16 } }}
                placeholder="Loading"
            />}
        />
    }




    return (
        <Autocomplete
            freeSolo
            disabled={isLoading}
            disablePortal
            options={models}
            multiple={false}
            sx={{
                width: 300, backgroundColor: "white",
                marginBottom: "20px"
            }}
            onChange={handleAutocompleteChange}
            renderInput={(params) => <TextField {...params}
                sx={{ "& .MuiInputBase-root": { fontSize: 16 } }}
                placeholder="Artist" />}
        />
    )
}

export default CustomAutocomplete;